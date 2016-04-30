class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/monitor'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SQLALCHEMY_ECHO = False

