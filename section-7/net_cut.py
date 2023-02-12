#!/usr/bin/env python

from netfilterqueue import NetfilterQueue


def process_packet(packet):
    print(packet)


queue = NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
