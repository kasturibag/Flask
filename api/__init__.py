from flask import Flask
from flask_restx import Api
from .author.views import author_namespace
from .auth.views import auth_namespace
from .book.views import book_namespace
from .config.config import DevConfig
from .models.users import User
from .models.authors import Author
from .models.books import Book
from .utils.db import db
from .utils.token import authorizations
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed
from http import HTTPStatus

def create_app(config=DevConfig):
    # initialize instance of flask app
    app = Flask(__name__)

    # app config using config object
    app.config.from_object(config)

    # app config using settings.py file
    # app.config.from_pyfile('settings.py')

    ## MYSQL connection
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/productdb'

    # configure api documentation
    api = Api(app,
        title="BookStore API",
        description="A REST API for a BookStore service",
        authorizations=authorizations,
    )

    # register api routes on api documentation
    api.add_namespace(author_namespace,)
    api.add_namespace(book_namespace,)
    api.add_namespace(auth_namespace,path='/auth')

    # configure database
    db.init_app(app)

    # configure jwt
    jwt=JWTManager(app)

    # error handling for not found
    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    # error handling for invalid http method
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method not allowed"},HTTPStatus.METHOD_NOT_ALLOWED

    #  to create all tables on database
    with app.app_context():
        db.create_all()


    return app