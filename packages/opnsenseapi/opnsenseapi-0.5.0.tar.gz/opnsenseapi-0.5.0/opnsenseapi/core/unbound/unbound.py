from opnsenseapi.core.unbound.settings.settings import Settings, _Settings
from opnsenseapi.ifaces.opnsense import _OpnSense


class _Unbound:
    def settings(self) -> _Settings:
        pass


class Unbound(_Unbound):
    ctrl: _OpnSense
    module: str

    def __init__(self, ctrl: _OpnSense):
        self.ctrl = ctrl
        self.module = "unbound"

    def settings(self) -> _Settings:
        return Settings(self.ctrl, module=self.module)
