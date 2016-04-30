__author__ = 'stikks & kunsam002'

from asset.services import ServiceFactory
from asset.models import *
from asset import db
from sqlalchemy import func

DeviceService = ServiceFactory.create_service(Device, db)
TransformerService = ServiceFactory.create_service(Transformer, db)
BaseReadingService = ServiceFactory.create_service(Reading, db)


class ReadingService(BaseReadingService):
    """ custom service class for saving readings from the remote sticks """
    @classmethod
    def create(cls, ignored_args=None, **kwargs):

        reference_code = kwargs.pop('device_code')
        device = Device.query.filter(func.lower(Device.reference_code) == reference_code.lower()).first()

        if not device:
            raise Exception('Device not found')

        kwargs['device_id'] = device.id

        model_number = kwargs.pop('transformer_model_number')
        if model_number:
            transformer = Transformer.query.filter(func.lower(Transformer.model_number) == model_number.lower()).first()

            if transformer:
                kwargs['transformer_id'] = transformer.id

        return BaseReadingService.create(ignored_args, **kwargs)

