from asset.resources import BaseResource, ModelListField, ModelField
from asset.services.assets import *
from asset.services.users import *
from asset.forms import *
from asset import register_api
from flask_restful import fields


class UtilityProviderResource(BaseResource):
    resource_name = 'utility-providers'
    service_class = UtilityProviderService
    validation_form = UtilityProviderForm
    resource_fields = {
        "name": fields.String,
        "url": fields.String
    }


class ConsumerResource(BaseResource):
    resource_name = 'consumers'
    service_class = ConsumerService
    validation_form = ConsumerForm
    resource_fields = {
        "first_name": fields.String,
        "last_name": fields.String,
        'address_id': fields.String,
        "utility_provider_id": fields.Integer(default=None),
        "address": ModelField,
        "utility_provider": ModelField
    }

    def adjust_form_fields(self, form):
        form.utility_provider_id.choices = [(c.id, c.name) for c in UtilityProvider.query.all()]

        return form

    def save(self, attrs, files=None):
        return ConsumerService.create(ignored_args=None, **attrs)


class DeviceResource(BaseResource):
    resource_name = 'devices'
    service_class = DeviceService
    validation_form = DeviceForm
    resource_fields = {
        "reference_code": fields.String,
        "meter_reference_code": fields.String,
        "consumer_id": fields.Integer(default=None),
        "utility_provider": fields.Integer(default=None),
        "is_master": fields.Boolean,
        "is_slave": fields.Boolean,
        "transformer_id": fields.Integer(default=None),
        "transformer": ModelField
    }

    def adjust_form_fields(self, form):
        form.consumer_id.choices = [(c.id, c.name) for c in Consumer.query.all()]
        form.transformer_id.choices = [(c.id, c.name) for c in Transformer.query.all()]
        form.utility_provider_id.choices = [(c.id, c.name) for c in UtilityProvider.query.all()]

        return form


class ReadingResource(BaseResource):
    resource_name = 'readings'
    service_class = ReadingService
    validation_form = ReadingForm
    resource_fields = {
        "degree": fields.Float,
        "humidity": fields.Float,
        "voltage": fields.Float,
        "current": fields.Float,
        "power": fields.Float,
        "device_id": fields.Integer,
        "device": ModelField,
        "transformer_id": fields.Integer(default=None),
        "transformer": ModelField
    }

    def save(self, attrs, files=None):
        return ReadingService.create(**attrs)


register_api(ConsumerResource, '/consumers', '/consumers/<int:id>', '/consumers/<int:id>/<string:resource_name>')
register_api(DeviceResource, '/devices', '/devices/<int:id>', '/devices/<int:id>/<string:resource_name>')
register_api(ReadingResource, '/readings', '/readings/<int:id>', '/readings/<int:id>/<string:resource_name>')
register_api(UtilityProviderResource, '/utility-providers', '/utility-providers/<int:id>', '/utility-providers/<string>')