#!/usr/bin/env python

import scapy.all as scapy


def sniff(interface, debug=False):
    scapy.sniff(iface=interface,
                store=True,  # whether to store results in memory
                prn=process_sniffed_packet)  # callback function

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if not real_mac == response_mac:
                print("[+] You are under attack!")
        except IndexError:
            pass


sniff(interface="eth0")
