from opnsenseapi.core.unbound.unbound import Unbound
from opnsenseapi.ifaces.opnsense import _OpnSense


class Core:
    ctrl: _OpnSense

    def __init__(self, ctrl: _OpnSense):
        self.ctrl = ctrl

    def get_unbound(self):
        return Unbound(self.ctrl)
