__author__ = 'stikks'

from asset.services import ServiceFactory
from asset.models import *
from asset import db

CountryService = ServiceFactory.create_service(Country, db)
StateService = ServiceFactory.create_service(State, db)
AddressService = ServiceFactory.create_service(Address, db)