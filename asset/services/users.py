__author__ = 'stikks & kunsam002'

from asset.models import *
from  sqlalchemy import or_, and_
from asset.services import ServiceFactory


UserService = ServiceFactory.create_service(User, db)
ConsumerService = ServiceFactory.create_service(Consumer, db)
UtilityProviderService = ServiceFactory.create_service(UtilityProvider, db)


def authenticate_user(username, password, **kwargs):
	"""
	Fetch a user based on the given username and password. 
	
	:param username: the username (or email address) of the user
	:param password: password credential
	:param kwargs: additional parameters required

	:returns: a user object or None
	"""
	user = User.query.filter(or_(User.username==username, User.email==username, User.active==True)).first()
	if user and user.check_password(password):
		return user
	else:
		return None
