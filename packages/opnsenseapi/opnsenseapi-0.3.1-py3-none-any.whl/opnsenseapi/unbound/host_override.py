import json
import math
from opnsenseapi.ifaces.opnsense import _OpnSense


class Host:
    id: str
    enabled: bool
    hostname: str
    domain: str
    rr: str
    mxprio: int
    mx: str
    server: str
    description: str

    def __init__(self,
                 enabled: bool,
                 hostname: str,
                 domain: str,
                 rr: str,
                 server: str,
                 description: str,
                 mxprio: int = None,
                 mx: str = None,
                 id: str = None):
        self.enabled = enabled
        self.hostname = hostname
        self.domain = domain
        self.rr = rr
        self.server = server
        self.description = description
        self.mx = mx
        if mxprio:
            self.mxprio = math.trunc(mxprio)
        else:
            self.mxprio = 0
        self.id = id

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return \
                    self.enabled == other.enabled and \
                    self.hostname == other.hostname and \
                    self.domain == other.domain and \
                    self.rr == other.rr and \
                    self.server == other.server and \
                    self.description == other.description and \
                    self.mx == other.mx and \
                    self.mxprio == other.mxprio and \
                    self.id == other.id
        return False

    def __str__(self):
        return f'Host is id={self.id} enabled={self.enabled} hostname={self.hostname} domain={self.domain} server={self.server}' \
               f' rr={self.rr} mx={self.mx} mxprio={self.mxprio} description={self.description}'


class HostOverride(object):
    ctrl: _OpnSense
    module = "unbound"
    controller = "settings"

    def __init__(self, ctrl: _OpnSense):
        self.ctrl = ctrl

    def create(self, host: Host):
        data = self.create_json_from_host(host)
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
        data = self.create_json_from_host(host)
        result = self.ctrl.modifying_request(self.module, self.controller, 'setHostOverride', data=data, params=[host.id])
        print(f"RES: {result}")
        if result['result'] == "saved":
            return host
        else:
            raise Exception(f"Error updating host: {result}")

    def delete_by_host(self, host: Host):
        return self.delete_by_id(host.id)

    def delete_by_id(self, id: str):
        result = self.ctrl.modifying_request(self.module, self.controller, 'delHostOverride', params=[id])
        if result['result'] == 'deleted':
            return True
        else:
            return False

    def get(self, id):
        return self.read(id)

    def list(self):
        result = self.ctrl.non_modifying_request(self.module, self.controller, 'searchHostOverride')
        print(result)

    def search(self):
        result = self.ctrl.non_modifying_request(self.module, self.controller, 'searchHostOverride')
        print(result)

    def create_host_from_json(self, result_json):
        host_json = result_json['host']
        if host_json['enabled'] == "1":
            enabled = True
        else:
            enabled = False
        if len(host_json['mxprio']) > 0:
            mxprio = host_json['mxprio']
        else:
            mxprio = None
        if len(host_json['mx']) > 0:
            mx = host_json['mx']
        else:
            mx = None
        h = Host(
            enabled=enabled,
            hostname=host_json['hostname'],
            domain=host_json['domain'],
            server=host_json['server'],
            description=host_json['description'],
            mxprio=mxprio,
            mx=mx,
            rr=host_json['rr']
        )
        return h

    def create_json_from_host(self, host: Host):
        enabled = 0
        if host.enabled:
            enabled = 1
        if not host.mx:
            mx = ""
        else:
            mx = host.mx
        if not host.mxprio:
            mxprio = ""
        else:
            mxprio = str(host.mxprio)

        h = {
            'host': {
                'enabled': str(enabled),
                'hostname': host.hostname,
                'domain': host.domain,
                'rr': host.rr,
                'mxprio': mxprio,
                'mx': mx,
                'server': host.server,
                'description': host.description
            }
        }
        return json.dumps(h, indent=2)
