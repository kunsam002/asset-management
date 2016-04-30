class Config:

	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/monitor'
	DATABASE = SQLALCHEMY_DATABASE_URI
	DEBUG = True
	SQLALCHEMY_ECHO = False