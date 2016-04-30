from asset.resources import BaseResource
from asset.services.assets import *
from asset.services.users import *
from asset.forms import *
from asset import register_api


class DeviceResource(BaseResource):
    resource_name = 'devices'
    service_class = DeviceService
    validation_form = DeviceForm
    resource_fields = {

    }
    def adjust_form_fields(self, form):
        form.utility_provider__id.choices = [(c.id, c.name) for c in UtilityProvider.query.all()]
        form.consumer_id.choices = [(c.id, c.name) for c in Consumer.query.all()]
        form.transormer_id.choices = [(c.id, c.name) for c in Transformer.query.all()]
        # form.cover_image_id.choices = [(c.id, c.url) for c in Image.query.filter(Image.merchant_id==merchant_id)]

        return form

# class ReadingResource(BaseResource):
#     resource_name = 'readings'
#     service_class = ReadingService
#     validation_form = ReadingForm
#     resource_fields = {
#
#     }
#
#
# class UtilityProviderResource(BaseResource):
#     resource_name = 'utility-providers'
#     service_class = UtilityProviderService
#     validation_form = UtilityProviderForm
#     resource_fields = {
#
#     }


register_api(DeviceResource, '/devices', '/devices/<int:id>', '/devices/<int:id>/<string:resource_name>')
# register_api(ReadingResource, '/readings', '/readings/<int:id>', '/readings/<int:id>/<string:resource_name>')
# register_api(UtilityProviderService, '/utilty-providers', '/utility-providers/<int:id>', '/utilty-providers/<string>')