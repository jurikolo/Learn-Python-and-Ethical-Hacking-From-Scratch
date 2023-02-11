#!/usr/bin/env python

import requests


target_url = "http://172.16.43.139/dvwa/login.php"
data_dict = {"username": "admin", "password": "password", "Login": "submit"}
response = requests.post(url=target_url, data=data_dict)
print(response.content)