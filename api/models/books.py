from ..utils.db import db
from ..models.authors import Author

class Book(db.Model):
    __tablename__= 'books'

    id=db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(25),nullable=False)
    author_id = db.Column(db.ForeignKey("authors.id"))
    author = db.relationship(Author, backref="books")

    def __str__(self):
        return f"<Book {self.id}>"


    def save(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)


    def delete(self):
        db.session.delete(self)
        db.session.commit()