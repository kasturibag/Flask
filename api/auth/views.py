from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash,check_password_hash
from http import HTTPStatus
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,get_jwt_identity)
from werkzeug.exceptions import Conflict,BadRequest
from ..utils.db import db

auth_namespace = Namespace('auth', description="Namespace for authentication")


signup_model=auth_namespace.model(
    'SignUp',{
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password"),
    }
)

user_model=auth_namespace.model(
    'User',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'password_hash':fields.String(required=True,description="A password"),
        'is_active':fields.Boolean(description="This shows that User is active"),
        'is_staff':fields.Boolean(description="This shows of use is staff")
    }
)

user_get_model=auth_namespace.model(
    'UserGet',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'is_active':fields.Boolean(description="This shows that User is active"),
        'is_staff':fields.Boolean(description="This shows of use is staff")
    }
)

user_input_model=auth_namespace.model(
    'UserInput',{
        'email':fields.String(required=True,description="An email"),
        'is_active':fields.Boolean(description="This shows that User is active"),
        'is_staff':fields.Boolean(description="This shows of use is staff")
    }
)

login_model=auth_namespace.model(
    'Login',{
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password")
    }
)


@auth_namespace.route('/signup')
class Signup(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
            Create new user account
        """

        data = request.get_json()

        try:


            new_user=User(
                username=data.get('username'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password'))
            )

            new_user.save()

            return new_user , HTTPStatus.CREATED

        except Exception as e:
            raise Conflict(f"User with email {data.get('email')} exists")


@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT pair
        """

        data=request.get_json()


        email=data.get('email')
        password=data.get('password')

        user=User.query.filter_by(email=email).first()


        if (user is not None) and check_password_hash(user.password_hash,password):
            access_token=create_access_token(identity=user.username)
            refresh_token=create_refresh_token(identity=user.username)

            response={
                'acccess_token':access_token,
                'refresh_token':refresh_token
            }

            return response, HTTPStatus.OK


        raise BadRequest("Invalid Username or password")


@auth_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        username=get_jwt_identity()


        access_token=create_access_token(identity=username)

        return {'access_token':access_token},HTTPStatus.OK


@auth_namespace.route('/user')
class AuthorGetUpdate(Resource):

    @auth_namespace.marshal_with(user_get_model)
    @auth_namespace.doc(
        description="Retrieve current user",
        security="jsonWebToken",
    )
    @jwt_required()
    def get(self):
        """
            Get current user
        """

        username=get_jwt_identity()
        current_user=User.query.filter_by(username=username).first()
        # author=Author.get_by_id(author_id)


        return current_user ,HTTPStatus.OK

    @auth_namespace.expect(user_input_model)
    @auth_namespace.marshal_with(user_input_model)
    @auth_namespace.doc(
        description="Update current user",
        security="jsonWebToken",
    )
    @jwt_required()
    def put(self):
        """
            Update current user
        """
        username=get_jwt_identity()
        user_to_update=User.query.filter_by(username=username).first()

        data=auth_namespace.payload

        user_to_update.email=data['email']
        user_to_update.is_active=data['is_active']
        user_to_update.is_staff=data['is_staff']


        db.session.commit()

        return user_to_update, HTTPStatus.OK
