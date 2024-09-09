from flask_restx import Namespace,Resource,fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..models.authors import Author
from http import HTTPStatus
from ..utils.db import db
from flask import request
# from ..utils.token import authorizations


author_namespace = Namespace('author', description='Namespace for author')

author_model=author_namespace.model(
    'Author',{
        'id':fields.Integer(),
        'name':fields.String(description="A name"),
        'city':fields.String(description="A city")
    }
)

author_input_model = author_namespace.model("AuthorInput", {
    'name':fields.String(required=True,description="A name"),
    'city':fields.String(required=True,description="A city")
})

# @author_namespace.route('/')
# class HelloAuthor(Resource):

#     def get(self):
#         return {"message": "Hello order"}


@author_namespace.route('/authors')
class AuthorGetCreate(Resource):

    @author_namespace.marshal_with(author_model)
    @author_namespace.doc(
        description="Retrieve all authors",
        security="jsonWebToken"
    )
    @jwt_required()
    def get(self):
        """
            Get all authors
        """
        authors=Author.query.all()

        return authors ,HTTPStatus.OK


    @author_namespace.expect(author_input_model)
    @author_namespace.marshal_with(author_model)
    @author_namespace.doc(
        description="Create an author",
        security="jsonWebToken"
    )
    @jwt_required()
    def post(self):
        """
            Create new author
        """
        # data = request.get_json()
        data=author_namespace.payload

        try:

            new_author=Author(
                name=data.get('name'),
                city=data.get('city'),
            )

            new_author.save()

            return new_author , HTTPStatus.CREATED

        except Exception as e:
            raise Conflict(f"Something went wrong while creating author")


@author_namespace.route('author/<int:author_id>/')
class AuthorGetUpdateDelete(Resource):

    @author_namespace.marshal_with(author_model)
    @author_namespace.doc(
        description="Retrieve an author by ID",
        security="jsonWebToken",
        params={
            "author_id":"An ID for a given author"
        }
    )
    @jwt_required()
    def get(self, author_id):
        """
            Get author by id
        """
        author=Author.get_by_id(author_id)


        return author ,HTTPStatus.OK

    @author_namespace.expect(author_model)
    @author_namespace.marshal_with(author_model)
    @author_namespace.doc(
        description="Update an author given an author ID",
        security="jsonWebToken",
        params={
            "author_id":"An ID for a given author"
        }
    )
    @jwt_required()
    def put(self, author_id):
        """
            Update author by id
        """
        author_to_update=Author.get_by_id(author_id)

        data=author_namespace.payload

        author_to_update.name=data['name']
        author_to_update.city=data['city']

        db.session.commit()

        return author_to_update, HTTPStatus.OK


    @author_namespace.marshal_with(author_model)
    @author_namespace.doc(
        description="Delete an author given an author ID",
        security="jsonWebToken",
        params={
            "author_id":"An ID for a given order"
        }
    )
    @jwt_required()
    def delete(self, author_id):
        """
            Delete author by id
        """

        author_to_delete=Author.get_by_id(author_id)

        author_to_delete.delete()

        return author_to_delete ,HTTPStatus.NO_CONTENT