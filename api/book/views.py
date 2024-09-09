from flask_restx import Namespace,Resource,fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..models.books import Book
from http import HTTPStatus
from ..utils.db import db
from flask import request
from ..author.views import author_model
# from ..utils.token import authorizations


book_namespace = Namespace('book', description='Namespace for book')

book_model=book_namespace.model(
    'Book',{
        'id':fields.Integer(),
        'name':fields.String(description="A name"),
        'author_id': fields.Integer(description="A author id"),
        'author': fields.Nested(author_model)
    }
)

book_input_model = book_namespace.model("BookInput", {
    'name':fields.String(required=True,description="A name"),
    'author_id':fields.Integer(required=True,description="A author_id")
})

# @author_namespace.route('/')
# class HelloAuthor(Resource):

#     def get(self):
#         return {"message": "Hello order"}


@book_namespace.route('/books')
class BookGetCreate(Resource):

    @book_namespace.marshal_with(book_model)
    @book_namespace.doc(
        description="Retrieve all books",
        security="jsonWebToken"
    )
    @jwt_required()
    def get(self):
        """
            Get all books
        """
        books=Book.query.all()

        return books ,HTTPStatus.OK


    @book_namespace.expect(book_input_model)
    @book_namespace.marshal_with(book_model)
    @book_namespace.doc(
        description="Create an book",
        security="jsonWebToken"
    )
    @jwt_required()
    def post(self):
        """
            Create new book
        """
        # data = request.get_json()
        data=book_namespace.payload

        try:

            new_book=Book(
                name=data.get('name'),
                author_id=data.get('author_id'),
            )

            new_book.save()

            return new_book, HTTPStatus.CREATED

        except Exception as e:
            raise Conflict(f"Something went wrong while creating author")


@book_namespace.route('book/<int:book_id>/')
class BookGetUpdateDelete(Resource):

    @book_namespace.marshal_with(book_model)
    @book_namespace.doc(
        description="Retrieve an book by ID",
        security="jsonWebToken",
        params={
            "book_id":"An ID for a given book"
        }
    )
    @jwt_required()
    def get(self, book_id):
        """
            Get book by id
        """
        book=Book.get_by_id(book_id)


        return book ,HTTPStatus.OK

    @book_namespace.expect(book_input_model)
    @book_namespace.marshal_with(book_model)
    @book_namespace.doc(
        description="Update an book given an book ID",
        security="jsonWebToken",
        params={
            "book_id":"An ID for a given book"
        }
    )
    @jwt_required()
    def put(self, book_id):
        """
            Update book by id
        """
        book_to_update=Book.get_by_id(book_id)

        data=book_namespace.payload

        book_to_update.name=data['name']
        book_to_update.author_id=data['author_id']

        db.session.commit()

        return book_to_update, HTTPStatus.OK


    @book_namespace.marshal_with(book_model)
    @book_namespace.doc(
        description="Delete an book given an book ID",
        security="jsonWebToken",
        params={
            "book_id":"An ID for a given book"
        }
    )
    @jwt_required()
    def delete(self, book_id):
        """
            Delete book by id
        """

        book_to_delete=Book.get_by_id(book_id)

        book_to_delete.delete()

        return book_to_delete ,HTTPStatus.NO_CONTENT