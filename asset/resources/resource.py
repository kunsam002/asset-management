from asset.resources import BaseResource
from asset.services.assets import DeviceService
from asset.forms import *


class DeviceResource(BaseResource):
    resource_name = 'device'
    service_class = DeviceService
    validation_form = DeviceForm
    resource_fields = {

    }
        