import threading

import requests
import urllib3
from requests.auth import HTTPBasicAuth

import opnsenseapi.unbound.host_override
from opnsenseapi.ifaces.opnsense import _OpnSense


class OpnSense(_OpnSense):
    opnsense_address: str
    opnsense_key: str
    opnsense_secret: str
    semaphore = threading.Semaphore(1)
    verify_cert: bool
    auth: HTTPBasicAuth

    def __init__(self, opnsense_address: str, opnsense_key: str, opnsense_secret: str, verify_cert: bool = True):
        if not opnsense_address:
            raise Exception("Address is missing")
        if not opnsense_address.startswith("https://"):
            opnsense_address = f"https://{opnsense_address}"
        if opnsense_address.endswith("/"):
            opnsense_address = opnsense_address[:-1]
        self.opnsense_address = opnsense_address
        if not opnsense_key:
            raise Exception("Key is missing")
        self.opnsense_key = opnsense_key
        if not opnsense_secret:
            raise Exception("Secret is missing")
        self.opnsense_secret = opnsense_secret
        self.verify_cert = verify_cert
        self.auth = HTTPBasicAuth(self.opnsense_key, self.opnsense_secret)

    def modifying_request(self, module: str, controller: str, command: str, data: str = None, params: list[str] = None):
        with self.semaphore:
            if not self.verify_cert:
                urllib3.disable_warnings()
            if params:
                p = ""
                for item in params:
                    p = p + f"/{item}"
                url = f"{self.opnsense_address}/api/{module}/{controller}/{command}{p}"
            else:
                url = f"{self.opnsense_address}/api/{module}/{controller}/{command}"
            print(url)
            print(data)
            if command.startswith("del"):
                headers = {}
            else:
                headers = {
                    'Content-type': 'application/json'
                }
            r = requests.post(
                url,
                data=data,
                verify=self.verify_cert,
                auth=self.auth,
                headers=headers)
            print(r.status_code)
            return r.json()

    def non_modifying_request(self, module: str, controller: str, command: str, params: list[str] = None):
        if not self.verify_cert:
            urllib3.disable_warnings()
        if params:
            p = ""
            for item in params:
                p = p + f"/{item}"
            url = f"{self.opnsense_address}/api/{module}/{controller}/{command}{p}"
        else:
            url = f"{self.opnsense_address}/api/{module}/{controller}/{command}"
        print(url)
        r = requests.get(
            url,
            verify=self.verify_cert,
            auth=self.auth)
        return r.json()

    def unbound_host_overrides(self):
        return opnsenseapi.unbound.host_override.HostOverride(self)
