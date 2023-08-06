import json

from opnsenseapi.core.unbound.settings.models.hosts import Host, MXHost, AHost
from opnsenseapi.ifaces.opnsense import _OpnSense


class _HostOverride:
    def create(self, host: Host):
        pass

    def read(self, id: str):
        pass

    def update(self, host: Host):
        pass

    def delete_by_id(self, id: str):
        pass

    def delete_by_host(self, host: Host):
        pass

    def get(self, id):
        pass

    def list(self):
        pass

    def search(self):
        pass


class HostOverride(_HostOverride):
    ctrl: _OpnSense
    module: str
    controller: str

    def __init__(self, ctrl: _OpnSense, module="unbound", controller="settings"):
        self.ctrl = ctrl
        self.module = module
        self.controller = controller

    def create(self, host: Host):
        data = host.to_json()
        result = self.ctrl.modifying_request(self.module, self.controller, 'addHostOverride', data=data)
        if result['result'] == "saved":
            host.id = result['uuid']
            return host
        else:
            print(f"ERROR: {result}")
            return host

    def read(self, id: str):
        result = self.ctrl.non_modifying_request(self.module, self.controller, 'getHostOverride', params=[id])
        if len(result) > 0:
            return self.create_host_from_json(result)
        else:
            raise Exception("No hosts found.")

    def update(self, host: Host):
        data = host.to_json()
        result = self.ctrl.modifying_request(self.module, self.controller, 'setHostOverride', data=data,
                                             params=[host.id])
        print(f"RES: {result}")
        if result['result'] == "saved":
            return host
        else:
            raise Exception(f"Error updating host: {result}")

    def delete_by_id(self, id: str):
        result = self.ctrl.modifying_request(self.module, self.controller, 'delHostOverride', params=[id])
        if result['result'] == 'deleted':
            return True
        else:
            return False

    def delete_by_host(self, host: Host):
        return self.delete_by_id(host.id)

    def get(self, id):
        return self.read(id)

    def list(self):
        result = self.ctrl.non_modifying_request(self.module, self.controller, 'searchHostOverride')
        print(result)

    def search(self):
        result = self.ctrl.non_modifying_request(self.module, self.controller, 'searchHostOverride')
        print(result)

    def create_host_from_json(self, host):
        response = json.loads(host)['host']
        if response['rr']["A"]["selected"] == 1:
            return AHost.from_json(host)
        elif response['rr']["MX"]["selected"] == 1:
            return MXHost.from_json(host)
