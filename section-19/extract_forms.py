#!/usr/bin/env python

import requests
import urllib.parse
from bs4 import BeautifulSoup


def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "http://172.16.43.139/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)
parsed_html = BeautifulSoup(markup=response.content, features="html.parser")
forms_list = parsed_html.findAll("form")

for form in forms_list:
    action = form.get("action")
    post_url = urllib.parse.urljoin(target_url, action)
    method = form.get("method")

    inputs_list = form.findAll("input")
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            print("a")
        post_data[input_name] = input_value
    print(post_data)
    result = requests.post(url=post_url, data=post_data)
    print(result.content.decode())


