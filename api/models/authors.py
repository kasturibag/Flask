from ..utils.db import db

class Author(db.Model):
    __tablename__= 'authors'

    id=db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(25),nullable=False)
    city = db.Column(db.String(25),nullable=False)
    # email=db.Column(db.String(80),nullable=False,unique=True)
    # orders=db.relationship('Order',backref='user',lazy=True)

    def __str__(self):
        return f"<Author {self.id}>"


    def save(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)


    def delete(self):
        db.session.delete(self)
        db.session.commit()