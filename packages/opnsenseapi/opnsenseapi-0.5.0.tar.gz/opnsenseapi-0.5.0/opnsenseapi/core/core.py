from opnsenseapi.core.unbound.unbound import Unbound, _Unbound
from opnsenseapi.ifaces.opnsense import _OpnSense


class _Core:

    def unbound(self) -> _Unbound:
        pass


class Core:
    ctrl: _OpnSense

    def __init__(self, ctrl: _OpnSense):
        self.ctrl = ctrl

    def unbound(self) -> _Unbound:
        return Unbound(self.ctrl)
