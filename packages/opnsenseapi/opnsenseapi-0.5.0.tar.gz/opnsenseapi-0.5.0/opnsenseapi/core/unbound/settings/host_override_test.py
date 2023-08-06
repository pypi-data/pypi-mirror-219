import json
import unittest
import pook

from opnsenseapi.core.unbound.settings.host_override import HostOverride
from opnsenseapi.opnsense import OpnSense


class HostOverrideTest(unittest.TestCase):
    def test_get_ahost_success(self):
        response = {
            "host": {
                "enabled": "1",
                "hostname": "test01",
                "domain": "test.de",
                "rr": {
                    "A": {
                        "value": "A (IPv4 address)",
                        "selected": 1
                    },
                    "AAAA": {
                        "value": "AAAA (IPv6 address)",
                        "selected": 0
                    },
                    "MX": {
                        "value": "MX (Mail server)",
                        "selected": 0
                    }
                },
                "mxprio": "",
                "mx": "",
                "server": "10.10.10.10",
                "description": "My Test Host"
            }
        }
        pook.on()
        pook.get('https://fw:8443/api/unbound/settings/getHostOverride/existing', reply=200,
                 response_headers={'Server': 'nginx'},
                 response_json=response)
        os = OpnSense(opnsense_address="https://fw:8443", opnsense_secret="os-secret", opnsense_key="os-key")
        overr = HostOverride(os)
        result = overr.get("existing")
        print(result)

    def test_get_ahost_404(self):
        response = {
            "host": {
                "enabled": "1",
                "hostname": "test01",
                "domain": "test.de",
                "rr": {
                    "A": {
                        "value": "A (IPv4 address)",
                        "selected": 1
                    },
                    "AAAA": {
                        "value": "AAAA (IPv6 address)",
                        "selected": 0
                    },
                    "MX": {
                        "value": "MX (Mail server)",
                        "selected": 0
                    }
                },
                "mxprio": "",
                "mx": "",
                "server": "10.10.10.10",
                "description": "My Test Host"
            }
        }
        pook.on()
        pook.get('https://fw:8443/api/unbound/settings/getHostOverride/abc', reply=404,
                 response_headers={'Server': 'nginx'},
                 response_json=response)
        os = OpnSense(opnsense_address="https://fw:8443", opnsense_secret="os-secret",
                                           opnsense_key="os-key")
        overr = HostOverride(os)
        result = overr.get("abc")
        print(result)


if __name__ == '__main__':
    unittest.main()
