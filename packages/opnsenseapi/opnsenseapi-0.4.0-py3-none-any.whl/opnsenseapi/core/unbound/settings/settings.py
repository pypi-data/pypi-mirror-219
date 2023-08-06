from opnsenseapi.core.unbound.settings.host_override import HostOverride
from opnsenseapi.ifaces.opnsense import _OpnSense


class Settings:
    ctrl: _OpnSense

    def __init__(self, ctrl: _OpnSense):
        self.ctrl = ctrl

    def get_host_override(self):
        return HostOverride(self.ctrl)
