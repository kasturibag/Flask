from datetime import timedelta

class Config:
    SECRET_KEY='do-i-really-need-this'
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_SECRET_KEY='i-need-this'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI='mysql://root:@localhost/bookstore'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    DEBUG=True


# class TestConfig(Config):
#     TESTING=True
#     SQLALCHEMY_DATABASE_URI='mysql://root:@localhost/bookstore'
#     SQLALCHEMY_TRACK_MODIFICATIONS=False
#     SQLALCHEMY_ECHO=True