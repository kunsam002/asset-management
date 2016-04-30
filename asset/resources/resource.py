from asset.resources import BaseResource
from asset.services.assets import *
from asset.services.users import *
from asset.forms import *
from asset import register_api


class UtilityProviderResource(BaseResource):
    resource_name = 'utility-providers'
    service_class = UtilityProviderService
    validation_form = UtilityProviderForm
    resource_fields = {

    }


class ConsumerResource(BaseResource):
    resource_name = 'consumers'
    service_class = ConsumerService
    validation_form = ConsumerForm
    resource_fields = {

    }


class DeviceResource(BaseResource):
    resource_name = 'devices'
    service_class = DeviceService
    validation_form = DeviceForm
    resource_fields = {

    }

    def adjust_form_fields(self, form):
        form.consumer_id.choices = [(c.id, c.name) for c in Consumer.query.all()]
        form.transormer_id.choices = [(c.id, c.name) for c in Transformer.query.all()]
        form.utility_provider_id.choices = [(c.id, c.name) for c in UtilityProvider.query.all()]

        return form


class ReadingResource(BaseResource):
    resource_name = 'readings'
    service_class = ReadingService
    validation_form = ReadingForm
    resource_fields = {

    }

    def save(self, attrs, files=None):
        return ReadingService.create(**attrs)


register_api(ConsumerResource, '/consumers', '/consumers/<int:id>', '/consumers/<int:id>/<string:resource_name>')
register_api(DeviceResource, '/devices', '/devices/<int:id>', '/devices/<int:id>/<string:resource_name>')
register_api(ReadingResource, '/readings', '/readings/<int:id>', '/readings/<int:id>/<string:resource_name>')
register_api(UtilityProviderResource, '/utility-providers', '/utility-providers/<int:id>', '/utility-providers/<string>')