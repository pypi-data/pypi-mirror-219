#!/usr/bin/env python3

import sys

import dpkt
import twnet_parser.packet

def print_tw_packets(pcap):
    for _ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        if not isinstance(ip.data, dpkt.udp.UDP):
            continue
        udp_payload = ip.data.data
        try:
            packet = twnet_parser.packet.parse7(udp_payload)
        except:
            continue
        names = [msg.message_name for msg in packet.messages]
        print(', '.join(names))

if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} <pcap file>')
    exit(1)

with open(sys.argv[1], 'rb') as f:
    pcap = dpkt.pcap.Reader(f)
    print_tw_packets(pcap)
