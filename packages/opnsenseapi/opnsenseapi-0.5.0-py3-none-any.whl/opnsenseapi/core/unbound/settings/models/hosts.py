import math
import json


class Host:
    id: str
    enabled: bool
    hostname: str
    domain: str
    rr: str
    description: str

    def __init__(self,
                 enabled: bool,
                 hostname: str,
                 domain: str,
                 description: str,
                 rr: str,
                 id: str = None):
        self.enabled = enabled
        self.hostname = hostname
        self.domain = domain
        self.description = description
        self.rr = rr
        self.id = id

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return \
                    self.enabled == other.enabled and \
                    self.hostname == other.hostname and \
                    self.domain == other.domain and \
                    self.rr == other.rr and \
                    self.description == other.description and \
                    self.id == other.id
        return False

    def __str__(self):
        return f'Host is id={self.id} enabled={self.enabled} hostname={self.hostname} domain={self.domain}' \
               f' rr={self.rr} description={self.description}'

    def from_json(self, result_json):
        host_json = result_json['host']
        if host_json['enabled'] == "1":
            enabled = True
        else:
            enabled = False
        h = Host(
            enabled=enabled,
            hostname=host_json['hostname'],
            domain=host_json['domain'],
            description=host_json['description'],
            rr=host_json['rr']
        )
        return h

    def to_json(self):
        if self.enabled:
            enabled = 1

        h = {
            'host': {
                'enabled': str(enabled),
                'hostname': self.hostname,
                'domain': self.domain,
                'rr': self.rr,
                'description': self.description
            }
        }
        return h


class AHost(Host):
    server: str

    def __init__(self,
                 enabled: bool,
                 hostname: str,
                 domain: str,
                 description: str,
                 server: str,
                 id: str = None):
        super().__init__(enabled=enabled, hostname=hostname, domain=domain, description=description, rr="A", id=id)
        self.server = server

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return \
                    super().__eq__(other) and \
                    self.server == other.server
        return False

    def __str__(self):
        return f'AHost is id={self.id} enabled={self.enabled} hostname={self.hostname} domain={self.domain} server={self.server}' \
               f' rr={self.rr} description={self.description}'

    @classmethod
    def from_dict(cls, result_json):
        host_json = result_json['host']
        if host_json['enabled'] == "1":
            enabled = True
        else:
            enabled = False
        h = cls(
            enabled=enabled,
            hostname=host_json['hostname'],
            domain=host_json['domain'],
            description=host_json['description'],
            server=host_json['server'],
        )
        return h

    @classmethod
    def from_json(cls, result_json):
        return cls.from_dict(json.loads(result_json))

    def to_json(self):
        h = super().to_json()
        h['host']['server'] = self.server
        return json.dumps(h, indent=2)


class MXHost(Host):
    id: str
    enabled: bool
    hostname: str
    domain: str
    rr: str
    mxprio: int
    mx: str
    description: str

    def __init__(self,
                 enabled: bool,
                 hostname: str,
                 domain: str,
                 description: str,
                 mx: str,
                 mxprio: int = 0,
                 id: str = None):
        super().__init__(enabled=enabled, hostname=hostname, domain=domain, description=description, rr="MX", id=id)
        self.mx = mx
        if mxprio:
            self.mxprio = math.trunc(mxprio)
        else:
            self.mxprio = 0

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return \
                    super().__eq__(other) and \
                    self.mx == other.mx and \
                    self.mxprio == other.mxprio
        return False

    def __str__(self):
        return f'Host is {super().__str__()} mx={self.mx} mxprio={self.mxprio} description={self.description}'

    @classmethod
    def from_dict(cls, result_dict):
        host_json = result_dict['host']
        if host_json['enabled'] == "1":
            enabled = True
        else:
            enabled = False
        if len(host_json['mxprio']) > 0:
            mx_prio = host_json['mxprio']
        else:
            mx_prio = None
        if len(host_json['mx']) > 0:
            mx = host_json['mx']
        else:
            mx = None
        h = cls(
            enabled=enabled,
            hostname=host_json['hostname'],
            domain=host_json['domain'],
            description=host_json['description'],
            mxprio=int(mx_prio),
            mx=mx
        )
        return h

    @classmethod
    def from_json(cls, result_json):
        return cls.from_dict(json.loads(result_json))


    def to_json(self):
        h = super().to_json()
        if not self.mx:
            mx = ""
        else:
            mx = self.mx
        if not self.mxprio:
            mx_prio = ""
        else:
            mx_prio = str(self.mxprio)
        h['host']['rr'] = self.rr
        h['host']['mx'] = mx
        h['host']['mxprio'] = mx_prio
        return json.dumps(h, indent=2)
