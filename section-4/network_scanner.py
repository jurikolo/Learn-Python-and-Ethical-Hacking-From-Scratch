#!/usr/bin/env python

import kamene.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target subnet to scan")
    parser.add_argument("-d", "--debug", dest="debug", help="Debug")
    options = parser.parse_args()
    if not options.target:
        parser.error("\n[-] Please specify a network, use --help for details")
    return options


def scan(ip):
    # scapy.ls(scapy.ARP())  # list input parameters
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # ff:ff:ff:ff:ff:ff is a broadcast MAC
    arp_request_broadcast = broadcast/arp_request  # combine Ethernet packet and ARP request
    print(arp_request_broadcast.summary()) if options.debug else None
    print(arp_request_broadcast.show()) if options.debug else None
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered_list:
        client_list.append({"ip": element[1].psrc, "mac": element[1].hwsrc})
    return client_list


def print_result(result_list):
    line = "-----------------------------------------"
    print("IP\t\t\tMAC")
    print(line)
    for client in result_list:
        print(client.get("ip") + "\t\t" + client.get("mac"))
        print(line)


options = get_arguments()
print_result(scan(options.target))
