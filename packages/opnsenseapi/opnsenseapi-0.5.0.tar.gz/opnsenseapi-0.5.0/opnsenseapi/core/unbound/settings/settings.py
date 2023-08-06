from opnsenseapi.core.unbound.settings.host_override import HostOverride, _HostOverride
from opnsenseapi.ifaces.opnsense import _OpnSense


class _Settings:
    def host_override(self) -> _HostOverride:
        pass


class Settings(_Settings):
    ctrl: _OpnSense
    module: str
    controller: str

    def __init__(self, ctrl: _OpnSense, module="unbound"):
        self.ctrl = ctrl
        self.module = module
        self.controller = "settings"

    def host_override(self) -> _HostOverride:
        return HostOverride(ctrl=self.ctrl, module=self.module, controller=self.controller)
