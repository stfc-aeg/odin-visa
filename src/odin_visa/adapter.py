from odin_visa.controller import VisaController
from odin_control.adapters.adapter import ApiAdapter


class VisaAdapter(ApiAdapter):

    version = '0.1'
    controller_cls = VisaController
