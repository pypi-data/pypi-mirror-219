import json
import unittest
from grappa import should

from opnsenseapi.core.unbound.settings.models.hosts import MXHost
from opnsenseapi.core.unbound.settings.models.hosts import AHost


class HostsTestCase(unittest.TestCase):
    def test_A_host_to_json(self):
        asset = AHost(enabled=1, hostname="hostname", domain="test.de", description="test-description", server="10.10.10.10")
        result = asset.to_json()
        value = json.loads(result)
        value | should.have.key("host")
        value['host'] | should.have.key("enabled").which.expect.to.be.equal("1")
        value['host'] | should.have.key("hostname").which.expect.to.be.equal("hostname")
        value['host'] | should.have.key("domain").which.expect.to.be.equal("test.de")
        value['host'] | should.have.key("rr").which.expect.to.be.equal("A")
        value['host'] | should.have.key("description").which.expect.to.be.equal("test-description")
        value['host'] | should.have.key("server").which.expect.to.be.equal("10.10.10.10")

    def test_A_host_from_json(self):
        expected = AHost(enabled=1, hostname="test01", domain="test.de", description="My Test Host",
                      server="10.10.10.10")
        mxprio_ = """{
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
        }"""
        result = AHost.from_json(mxprio_)
        result | should.be.equal.to(expected)

    def test_MX_host_to_json(self):
        asset = MXHost(enabled=1, hostname="hostname", domain="test.de", description="test-description",
                      mx="hostname.test.de",mxprio=10)
        result = asset.to_json()
        v = json.loads(result)
        print(v)
        v | should.have.key("host")
        v['host'] | should.have.key("enabled").which.expect.to.be.equal("1")
        v['host'] | should.have.key("hostname").which.expect.to.be.equal("hostname")
        v['host'] | should.have.key("domain").which.expect.to.be.equal("test.de")
        v['host'] | should.have.key("rr").which.expect.to.be.equal("MX")
        v['host'] | should.have.key("description").which.should.be.equal.to("test-description")
        v['host'] | should.have.key("mx").which.expect.to.be.equal("hostname.test.de")
        v['host'] | should.have.key("mxprio").which.expect.to.be.equal("10")

    def test_MX_host_from_json(self):
        expected = MXHost(enabled=True, hostname="hostname", domain="test.de", description="test-description",
                      mxprio=10, mx="test.test.de")
        mxprio_ = """{
        "host": {
            "enabled": "1", 
            "hostname": "hostname", 
            "domain": "test.de", 
            "rr": "MX", 
            "description": 
            "test-description", 
            "mx": "test.test.de", 
            "mxprio": "10"
            }
        }
        """
        result = MXHost.from_json(mxprio_)
        result | should.be.equal.to(expected)

if __name__ == '__main__':
    unittest.main()
