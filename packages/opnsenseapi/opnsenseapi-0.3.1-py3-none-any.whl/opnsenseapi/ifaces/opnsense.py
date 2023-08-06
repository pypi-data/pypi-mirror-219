class _OpnSense:
    def modifying_request(self, module: str, controller: str, command: str, data: str = None, params: list[str] = None):
        pass

    def non_modifying_request(self, module: str, controller: str, command: str,
                              params: list[str] = None):
        pass
