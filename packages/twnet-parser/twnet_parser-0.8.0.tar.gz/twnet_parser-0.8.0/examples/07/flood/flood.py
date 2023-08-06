#!/usr/bin/env python3

import socket
import sys
import time
from signal import signal, SIGINT
from typing import Optional

from twnet_parser.packet import TwPacket, parse7
from twnet_parser.messages7.control.token import CtrlToken
from twnet_parser.messages7.control.connect import CtrlConnect
from twnet_parser.messages7.control.close import CtrlClose
from twnet_parser.messages7.control.keep_alive import CtrlKeepAlive
from twnet_parser.messages7.system.info import MsgInfo
from twnet_parser.messages7.system.map_change import MsgMapChange
from twnet_parser.messages7.system.ready import MsgReady
from twnet_parser.messages7.game.cl_start_info import MsgClStartInfo
from twnet_parser.messages7.system.enter_game import MsgEnterGame
# from twnet_parser.messages7.game.cl_kill import MsgClKill

from twnet_parser.constants import NET_MAX_PACKETSIZE, NET_MAX_SEQUENCE

if len(sys.argv) < 3:
    print("usage: flood.py HOST PORT [NUM_TEES]")
    print("description:")
    print("  connects to given server")
    print("  and keeps the connection alive")
    print("example:")
    print("  flood.py localhost 8303 2")
    exit(1)

class TeeworldsClient():
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port
        self.dest_srv = (self.host, self.port)

        self.log(f"Connecting to {host}:{port} ...")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 0))

        self.outfile = None
        self.downloaded_chunks = 0
        self.downloaded_bytes = 0
        self.sent_vital = 0
        self.got_vital = 0
        self.got_seqs = set()
        self.map_info: Optional[MsgMapChange] = None
        self.my_token = b'\xff\xaa\xbb\xee'
        self.srv_token = b'\xff\xff\xff\xff'
        self.last_send_time = time.time()

        # TODO: we should be able to set this
        # ctrl_token = CtrlToken(we_are_a_client = True)
        ctrl_token = CtrlToken()
        ctrl_token.response_token = self.my_token
        self.send_msg(ctrl_token)

    def log(self, message):
        print(f"[{self.name}] {message}")

    def send_msg(self, messages):
        if not isinstance(messages, list):
            messages = [messages]
        packet = TwPacket()
        packet.header.token = self.srv_token
        for msg in messages:
            if hasattr(msg, 'header'):
                if msg.header.flags.vital:
                    self.sent_vital += 1
                msg.header.seq = self.sent_vital
            packet.messages.append(msg)
        self.last_send_time = time.time()
        packet.header.ack = self.got_vital
        self.sock.sendto(packet.pack(), self.dest_srv)

    def tick(self):
        data, addr = self.sock.recvfrom(NET_MAX_PACKETSIZE)
        packet = parse7(data)

        for msg in packet.messages:
            self.log(f"got msg {msg.message_id}")
            if hasattr(msg, 'header'):
                if msg.header.flags.vital and not msg.header.flags.resend:
                    self.got_vital = (self.got_vital + 1) % NET_MAX_SEQUENCE
                if msg.header.seq in self.got_seqs:
                    continue
                self.got_seqs.add(msg.header.seq)

            if msg.message_name == 'token':
                self.srv_token = msg.response_token

                ctrl_connect = CtrlConnect()
                ctrl_connect.response_token = self.my_token
                self.send_msg(ctrl_connect)
            elif msg.message_name == 'accept':
                info = MsgInfo()
                info.header.flags.vital = True
                self.send_msg(info)
            elif msg.message_name == 'map_change' or msg.message_name == 'map_data':
                ready = MsgReady()
                ready.header.flags.vital = True
                self.send_msg(ready)
            elif msg.message_name == 'con_ready':
                self.log("sending info")
                startinfo = MsgClStartInfo()
                startinfo.header.flags.vital = True
                self.send_msg(startinfo)
                enter_game = MsgEnterGame()
                enter_game.header.flags.vital = True
                self.send_msg(enter_game)
            elif msg.message_name == 'close':
                self.log(f"disconnected reason='{msg.reason}'")
                exit(1)

        if (time.time() - self.last_send_time) > 1:
            self.send_msg(CtrlKeepAlive())
            # kill = MsgClKill()
            # kill.header.flags.vital = True
            # self.send_msg(kill)

num_clients = 1
if len(sys.argv) > 3:
    num_clients = int(sys.argv[3])
clients = []

for i in range(0, num_clients):
    client = TeeworldsClient(name = i, host = sys.argv[1], port = int(sys.argv[2]))
    clients.append(client)

def handler(signal_received, frame):
    global clients
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    for client in clients:
        close = CtrlClose()
        client.log("sending disconnect")
        client.send_msg(close)
    exit(0)

signal(SIGINT, handler)

while True:
    for client in clients:
        client.tick()

