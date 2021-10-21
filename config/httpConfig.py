import requests, configparser,os, urllib3
from config.logConfig import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = configparser.ConfigParser()
config.read("./config.ini", encoding="utf-8")

class HttpConfig:
    timeout = config["api"]["timeout"]

    def __init__(self):
        self.logger = logger()
        self.url = config["api"]["url"]
        self.headers = {"Content-Type" : "application/json"}

    def get(self,api_url,headers,body=None):
        try:
            url = self.url + api_url
            self.logger.INFO(f"请求方式：Get,Url={url}")
            resp = requests.get(url=url,headers=headers, verify=False, timeout = float(self.timeout))

            return resp
        except TimeoutError:
            self.logger.ERROR("Time out！")
            return None

    def post(self, api_url, body, headers = None):
        try:
            url = self.url + api_url
            self.logger.INFO(f"请求方式：Post,Url={url}")
            if not headers:
                resp = requests.post(url=url, headers=self.headers, json=body, verify=False, timeout=float(self.timeout))
            else:
                resp = requests.post(url=url, headers=headers, json=body, verify=False,
                                     timeout=float(self.timeout))

            return resp
        except TimeoutError:
            self.logger.ERROR("Time out！")
            return None