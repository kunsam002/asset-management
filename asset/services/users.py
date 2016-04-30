__author__ = 'stikks'

from asset.services import ServiceFactory
from asset.models import *
from asset import db

UtilityProviderService = ServiceFactory.create_service(UtilityProvider, db)
ConsumerService = ServiceFactory.create_service(Consumer, db)