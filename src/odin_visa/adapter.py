from odin_control.adapters.async_adapter import AsyncApiAdapter

from odin_visa.controller import VisaController


class VisaAdapter(AsyncApiAdapter):

    version = "0.1"
    controller_cls = VisaController
