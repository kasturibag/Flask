from datetime import timedelta

DEBUG=True
SQLALCHEMY_DATABASE_URI='mysql://root:@localhost/bookstore'
SQLALCHEMY_TRACK_MODIFICAIONS=False
SQLALCHEMY_ECHO=True
SECRET_KEY='abcde12345'
JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)
JWT_SECRET_KEY='12345'