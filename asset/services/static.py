__author__ = 'stikks'

from asset.services import ServiceFactory
from asset.models import *
from asset import db

CountryService = ServiceFactory(Country, db)
StateService = ServiceFactory(State, db)
AddressService = ServiceFactory(Address, db)