__author__ = 'stikks & kunsam002'

from asset.services import ServiceFactory
from asset.models import *
from asset import db

DeviceService = ServiceFactory(Device, db)
TransformerService = ServiceFactory(Transformer, db)
