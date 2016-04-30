__author__ = 'stikks & kunsam002'

from asset.services import ServiceFactory
from asset.models import *
from asset import db

DeviceService = ServiceFactory.create_service(Device, db)
TransformerService = ServiceFactory.create_service(Transformer, db)
ReadingService = ServiceFactory.create_service(Reading, db)

