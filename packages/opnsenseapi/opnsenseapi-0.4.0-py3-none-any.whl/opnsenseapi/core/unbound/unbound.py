from opnsenseapi.core.unbound.settings.settings import Settings
from opnsenseapi.ifaces.opnsense import _OpnSense


class Unbound:
    ctrl: _OpnSense

    def __init__(self, ctrl: _OpnSense):
        self.ctrl = ctrl

    def get_settings(self):
        return Settings(self.ctrl)
