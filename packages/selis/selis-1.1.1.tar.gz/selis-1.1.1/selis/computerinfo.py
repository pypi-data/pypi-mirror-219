import requests
import platform


class ComputerInfo:
    def __init__(self):
        self.url = "https://ipinfo.io/json"


    def get_public_ip(self):
        response = requests.get(self.url)
        public_ip = response.json()["ip"]
        return public_ip


    def get_system_info(self):
        return platform.machine() + "/" + platform.node() + "/" + platform.platform() + "/" + platform.processor() + "/" + \
            platform.release() + "/" + platform.system() + "/" + platform.version()


    def get(self):
        public_ip = self.get_public_ip()
        os_info = self.get_system_info()

        return public_ip + "/" + os_info
    