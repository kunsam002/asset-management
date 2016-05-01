__author__ = 'stikks & kunsam002'

from asset.models import *
from  sqlalchemy import or_, and_
from asset.services import ServiceFactory
from .static import AddressService

UserService = ServiceFactory.create_service(User, db)
BaseConsumerService = ServiceFactory.create_service(Consumer, db)
UtilityProviderService = ServiceFactory.create_service(UtilityProvider, db)


class ConsumerService(BaseConsumerService):
    @classmethod
    def create(cls, ignored_args=None, **kwargs):
        name = kwargs.pop("name")
        utility_provider_id = kwargs.pop("utility_provider_id")

        address = AddressService.create_service(ignored_args, **kwargs)

        data = {
            "name": name,
            "utility_provider_id": utility_provider_id,
            "address_id": address.id
        }

        return BaseConsumerService.create(ignored_args, **data)


def authenticate_user(username, password, **kwargs):
    """
    Fetch a user based on the given username and password.

    :param username: the username (or email address) of the user
    :param password: password credential
    :param kwargs: additional parameters required

    :returns: a user object or None
    """
    user = User.query.filter(or_(User.username == username, User.email == username, User.active == True)).first()
    if user and user.check_password(password):
        return user
    else:
        return None
