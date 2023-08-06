import requests
import os
import json
import urllib
import getpass
import time
import configparser
import re
import sys

class RequestInfoException(Exception):
    pass

class Client:
    def __init__(
            self, 
            config_file_location_v2: str ='~/.brmconfig'
        ) -> None:

        self.openapi_host = os.getenv("OPENAPI_HOST", "https://openapi.dp.tech")
        self.config_file_location_expand = os.path.expanduser(config_file_location_v2)
        self.ticket = os.environ.get("BHOR_TICKET", "")
        if not os.path.exists(self.config_file_location_expand) and self.ticket == "":
            weburl = self.openapi_host.replace("openapi", "bohrium")
            print(f"Config File ~/.brmconfig not found! Please visit {weburl}/personal/setting and click AccessKey create button to generate it !")
            self.access_key = input("Please enter AccessKey: ")
            data = f"[Credentials]\naccessKey={self.access_key}"
            with open(self.config_file_location_expand, 'w') as f:
                f.write(data)
        config = configparser.ConfigParser()
        config.read(self.config_file_location_expand)
        self.base_url = self.openapi_host
        self.access_key = config.get('Credentials', 'accessKey')
        self.params = {"accessKey": self.access_key}
        self.token = ""
        self.check_ak()
            

    def post(self, url, host="", json=None, data=None, headers=None, params=None, stream=False, retry=5):
        return self._req('POST', url, host=host, json=json, data=data, headers=headers, params=params, stream=stream, retry=retry)

    def get(self, url, host="", json=None, headers=None, params=None, stream=False, retry=5):
        return self._req('GET', url, host=host, json=json, headers=headers, params=params, stream=stream, retry=retry)

    def _req(self, method, url, host="", json=None, data=None, headers=None, params=None, stream=False, retry=3):
        if host: #in ["https://bohrium.test.dp.tech", "https://tiefblue.test.dp.tech"]:
            url = urllib.parse.urljoin(host, url)
        else:
            url = urllib.parse.urljoin(self.base_url, url)
        
        # Set Headers
        if headers is None: headers = {}
       
        if self.token: headers['Authorization'] = f'Bearer {self.token}'
        if self.ticket: headers['Brm-Ticket'] = self.ticket
        
        # headers['bohr-client'] = f'utility:0.0.2'
        resp_code = None
        for i in range(retry):
            resp = None
            err = ""
            if method == 'GET':
                resp = requests.get(url=url, params=params, headers=headers, stream=stream)
            if method == 'POST':
                resp = requests.post(url=url, json=json, data=data, params=params, headers=headers, stream=stream)
            resp_code = resp.status_code
            if resp_code == 401:
                # os.remove(self.config_file_location_expand)
                weburl = self.openapi_host.replace("openapi", "bohrium")
                print(f"Config file(~/.brmconfig) AccessKey invalid! Visit {weburl}/personal/setting to generate it! ")
                sys.exit()
            if not resp.ok:
                try:
                    result = resp.json()
                    err = result.get("error")
                except:
                    pass
                # time.sleep(0.1 * i)
                time.sleep(20)
                continue
            # print(resp.text)
            result = resp.json()
            if isinstance(result, str): return result
            if result.get('model', '') == 'gpt-35-turbo':
                return result['choices'][0]['message']['content']
            elif result['code'] == 0:
                return result.get('data', {})
            else:
                err = result.get("message") or result.get("error")
                break
        raise RequestInfoException(resp_code, url, err)

    # def get_token(self):
    #     self.login()
    #     return self.token

    def check_ak(self):
        url = f"/openapi/v1/ak/get"
        resp = self.get(url=url, params=self.params)
        if resp.get("user_id", 0) != 0:
            pass
            # print("AccessKey authorization passed! ")
        return resp

    # def login(self):
    #     email = input("Please enter Bohrium Account Email: ")
    #     password = getpass.getpass(prompt="Please enter password: ")
    #     post_data = {
    #         'username': email,
    #         'password': password
    #     }
    #     resp = requests.post('https://bohrium.dp.tech/account_gw/login', json=post_data).json().get("data", {})
    #     self.token = resp.get('token', '')
    #     if self.token: print("Login successfully!")
    #     else: print("Login failed!")

    # def generate_access_key(self, name="default"):
    #     post_data = { "name": name }
    #     headers = { 'Authorization': f'Bearer {self.token}' }
    #     resp = requests.post(url="https://bohrium-api.dp.tech/bohrapi/v1/ak/add", json=post_data, headers=headers)
    #     print(resp)
    #     resp = resp.json().get("data", {})
    #     self.access_key = resp.get("accessKey", "")
    #     data = f"[Credentials]\nbaseUrl=https://openapi.dp.tech\naccessKey={self.access_key}"
    #     with open(self.config_file_location_expand, 'w') as f:
    #         f.write(data)
    #     return resp


    def chat(self, prompt, temperature=0):
        post_data = {
            "messages":[{"role":"user","content":f"{prompt}"}],
            "stream":False,
            "model":"gpt-3.5-turbo",
            "temperature":temperature,
            "presence_penalty":0
        }

        resp = self.post(f"/openapi/v1/chat/complete", json=post_data, params=self.params)
        return resp
