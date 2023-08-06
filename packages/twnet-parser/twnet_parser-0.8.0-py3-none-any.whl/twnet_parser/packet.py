#!/usr/bin/env python

from typing import Union, cast, Optional, Literal

from twnet_parser.packer import Unpacker, pack_int
from twnet_parser.pretty_print import PrettyPrint
from twnet_parser.message_parser import MessageParser
from twnet_parser.net_message import NetMessage
from twnet_parser.ctrl_message import CtrlMessage
from twnet_parser.connless_message import ConnlessMessage
from twnet_parser.chunk_header import ChunkHeader, ChunkFlags
from twnet_parser.msg_matcher.control7 import match_control7
from twnet_parser.msg_matcher.connless7 import match_connless7
from twnet_parser.msg_matcher.control6 import match_control6
from twnet_parser.msg_matcher.connless6 import match_connless6
from twnet_parser.constants import NET_MAX_SEQUENCE, NET_PACKETVERSION

import twnet_parser.huffman

# TODO: what is a nice pythonic way of storing those?
#       also does some version:: namespace thing make sense?
PACKETFLAG7_CONTROL = 1
PACKETFLAG7_RESEND = 2
PACKETFLAG7_COMPRESSION = 4
PACKETFLAG7_CONNLESS = 8

PACKETFLAG6_UNUSED = 1
PACKETFLAG6_TOKEN = 2
PACKETFLAG6_CONTROL = 4
PACKETFLAG6_CONNLESS = 8
PACKETFLAG6_RESEND = 16
PACKETFLAG6_COMPRESSION = 32

CHUNKFLAG7_VITAL = 1
CHUNKFLAG7_RESEND = 2

PACKET_HEADER7_SIZE = 7
CONNLESS_PACKET_HEADER7_SIZE = 9
CONNLESS_PACKET_HEADER6_SIZE = 6

class PacketFlags7(PrettyPrint):
    def __init__(self) -> None:
        self.control: Optional[bool] = None
        self.resend: Optional[bool] = None
        self.compression: Optional[bool] = None
        self.connless: Optional[bool] = None

class PacketFlags6(PrettyPrint):
    def __init__(self) -> None:
        self.token: Optional[bool] = None
        self.control: Optional[bool] = None
        self.resend: Optional[bool] = None
        self.compression: Optional[bool] = None
        self.connless: Optional[bool] = None

class PacketHeader6(PrettyPrint):
    def __init__(
            self,
            flags: Optional[PacketFlags6] = None,
            ack: int = 0,
            token: bytes = b'\xff\xff\xff\xff',
            num_chunks: Optional[int] = None
    ) -> None:
        """
        If num_chunks is not set it will count
        the messages it was given when
        the pack() method is called
        """
        if not flags:
            flags = PacketFlags6()
        self.flags: PacketFlags6 = flags
        self.ack: int = ack % NET_MAX_SEQUENCE
        self.token: bytes = token
        self.num_chunks: Optional[int] = num_chunks

        # connless only
        self.connless_version: int = NET_PACKETVERSION
        self.response_token: bytes = b'\xff\xff\xff\xff'

    def pack(self) -> bytes:
        """
        Generate 7 byte teeworlds 0.6.5 packet header
        based on the current instance variable
        values.

        The layout is as follows
        6bit flags, 2bit ack
        8bit ack
        8bit chunks
        32bit token

        ffffffaa
        aaaaaaaa
        NNNNNNNN
        TTTTTTTT
        TTTTTTTT
        TTTTTTTT
        TTTTTTTT
        """
        flags = 0
        if self.flags.token is None:
            # do not automatically set the token flag
            # if the token field has the empty token value
            if self.token != b'\xff\xff\xff\xff':
                self.flags.token = True
        if self.flags.token:
            flags |= PACKETFLAG6_TOKEN
        if self.flags.control:
            flags |= PACKETFLAG6_CONTROL
        if self.flags.connless:
            flags |= PACKETFLAG6_CONNLESS
        if self.flags.resend:
            flags |= PACKETFLAG6_RESEND
        if self.flags.compression:
            flags |= PACKETFLAG6_COMPRESSION
        if self.num_chunks is None:
            self.num_chunks = 0
        if self.flags.connless:
            return b'\xff\xff\xff\xff\xff\xff'
        packed = bytes([ \
            ((flags << 2)&0xfc) | ((self.ack>>8)&0x03), \
            self.ack&0xff, \
            self.num_chunks \
        ])
        if self.flags.token:
            packed += self.token
        return packed

class PacketHeader(PrettyPrint):
    def __init__(
            self,
            flags: Optional[PacketFlags7] = None,
            ack: int = 0,
            token: bytes = b'\xff\xff\xff\xff',
            num_chunks: Optional[int] = None
    ) -> None:
        """
        If num_chunks is not set it will count
        the messages it was given when
        the pack() method is called
        """
        if not flags:
            flags = PacketFlags7()
        self.flags: PacketFlags7 = flags
        self.ack: int = ack % NET_MAX_SEQUENCE
        self.token: bytes = token
        self.num_chunks: Optional[int] = num_chunks

        # connless only
        self.connless_version: int = NET_PACKETVERSION
        self.response_token: bytes = b'\xff\xff\xff\xff'

    def pack(self) -> bytes:
        """
        Generate 7 byte teeworlds 0.7 packet header
        based on the current instance variable
        values.

        The layout is as follows
        6bit flags, 2bit ack
        8bit ack
        8bit chunks
        32bit token

        ffffffaa
        aaaaaaaa
        NNNNNNNN
        TTTTTTTT
        TTTTTTTT
        TTTTTTTT
        TTTTTTTT
        """
        flags = 0
        if self.flags.control:
            flags |= PACKETFLAG7_CONTROL
        if self.flags.resend:
            flags |= PACKETFLAG7_RESEND
        if self.flags.compression:
            flags |= PACKETFLAG7_COMPRESSION
        if self.flags.connless:
            flags |= PACKETFLAG7_CONNLESS
        if self.num_chunks is None:
            self.num_chunks = 0
        if self.flags.connless:
            return bytes([ \
                ((PACKETFLAG7_CONNLESS<<2)&0xfc) | (self.connless_version&0x03)
            ]) + self.token + self.response_token
        return bytes([ \
            ((flags << 2)&0xfc) | ((self.ack>>8)&0x03), \
            self.ack&0xff, \
            self.num_chunks \
        ]) + self.token

class TwPacket(PrettyPrint):
    def __init__(self, version: Literal['0.6', '0.7']= '0.7') -> None:
        self._version: Literal['0.6', '0.7'] = version
        self.payload_raw: bytes = b''
        self.payload_decompressed: bytes = b''
        self.header: Union[PacketHeader, PacketHeader6]
        if self.version == '0.6':
            self.header = PacketHeader6()
        elif self.version == '0.7':
            self.header = PacketHeader()
        else:
            raise ValueError(f"Error: invalid packet version '{self.version}'")
        self.messages: list[Union[CtrlMessage, NetMessage, ConnlessMessage]] = []

    @property
    def version(self) -> Literal['0.6', '0.7']:
        return self._version

    def pack(self, we_are_a_client = True) -> bytes:
        payload: bytes = b''
        msg: Union[CtrlMessage, NetMessage, ConnlessMessage]
        is_control: bool = False
        is_connless: bool = False
        for msg in self.messages:
            if msg.message_type == 'connless':
                is_connless = True
                msg = cast(ConnlessMessage, msg)
                payload += bytes(msg.message_id)
                payload += msg.pack()
            elif msg.message_type == 'control':
                is_control = True
                msg = cast(CtrlMessage, msg)
                payload += pack_int(msg.message_id)
                payload += msg.pack(we_are_a_client)
            else: # game or system message
                msg = cast(NetMessage, msg)
                msg_payload: bytes = pack_int(
                    (msg.message_id<<1) |
                    (int)(msg.system_message)
                )
                msg_payload += msg.pack()
                if msg.header.size is None:
                    msg.header.size = len(msg_payload)
                payload += msg.header.pack()
                payload += msg_payload
        if self.header.num_chunks is None:
            if is_control:
                self.header.num_chunks = 0
            else:
                self.header.num_chunks = len(self.messages)
        if is_control:
            if self.header.flags.control is None:
                self.header.flags.control = True
        if is_connless:
            if self.header.flags.connless is None:
                self.header.flags.connless = True
        if self.header.flags.compression:
            payload = twnet_parser.huffman.compress(payload)
        return self.header.pack() + payload

class PacketHeaderParser6():
    def parse_flags6(self, data: bytes) -> PacketFlags6:
        # FFFF FFaa
        flag_bits = data[0] >> 2
        flags = PacketFlags6()
        flags.token = (flag_bits & PACKETFLAG6_TOKEN) != 0
        flags.control = (flag_bits & PACKETFLAG6_CONTROL) != 0
        flags.connless = (flag_bits & PACKETFLAG6_CONNLESS) != 0
        flags.resend = (flag_bits & PACKETFLAG6_RESEND) != 0
        flags.compression = (flag_bits & PACKETFLAG6_COMPRESSION) != 0
        if flags.connless:
            # conless packets send FF
            # as the flag byte
            # but setting the connless bit basically means
            # all other flags are false implicitly
            flags.token = False
            flags.control = False
            flags.resend = False
            flags.compression = False
        return flags

    def parse_ack(self, header_bytes: bytes) -> int:
        # ffAA AAAA AAAA
        return ((header_bytes[0] & 0x3) << 8) | header_bytes[1]

    def parse_num_chunks(self, header_bytes: bytes) -> int:
        # TODO: not sure if this is correct
        return header_bytes[2]

    def parse_token(self, header_bytes: bytes) -> bytes:
        return header_bytes[3:7]

    def parse_header(self, data: bytes) -> PacketHeader6:
        header = PacketHeader6()
        # bits 1..5
        header.flags = self.parse_flags6(data)
        if header.flags.connless:
            # TODO: do not hardcode version field
            #       but actually read the bits
            header.connless_version = NET_PACKETVERSION
            header.token = data[1:5]
            header.response_token = data[5:9]
        else:
            # bits 6..16
            header.ack = self.parse_ack(data)
            # bits 17..25
            header.num_chunks = self.parse_num_chunks(data)
            # bits 16..57
            header.token = self.parse_token(data)
        return header

class PacketHeaderParser7():
    def parse_flags7(self, data: bytes) -> PacketFlags7:
        # FFFF FFaa
        flag_bits = (data[0] & 0xfc) >> 2
        flags = PacketFlags7()
        flags.control = (flag_bits & PACKETFLAG7_CONTROL) != 0
        flags.resend = (flag_bits & PACKETFLAG7_RESEND) != 0
        flags.compression = (flag_bits & PACKETFLAG7_COMPRESSION) != 0
        flags.connless = (flag_bits & PACKETFLAG7_CONNLESS) != 0
        return flags

    def parse_ack(self, header_bytes: bytes) -> int:
        # ffAA AAAA AAAA
        return ((header_bytes[0] & 0x3) << 8) | header_bytes[1]

    def parse_num_chunks(self, header_bytes: bytes) -> int:
        # TODO: not sure if this is correct
        return header_bytes[2]

    def parse_token(self, header_bytes: bytes) -> bytes:
        return header_bytes[3:7]

    def parse_header(self, data: bytes) -> PacketHeader:
        header = PacketHeader()
        # bits 2..5
        header.flags = self.parse_flags7(data)
        if header.flags.connless:
            # TODO: do not hardcode version field
            #       but actually read the bits
            header.connless_version = NET_PACKETVERSION
            header.token = data[1:5]
            header.response_token = data[5:9]
        else:
            # bits 6..16
            header.ack = self.parse_ack(data)
            # bits 17..25
            header.num_chunks = self.parse_num_chunks(data)
            # bits 16..57
            header.token = self.parse_token(data)
        return header

class ChunkHeaderParser:
    def parse_flags7(self, data: bytes) -> ChunkFlags:
        # FFss ssss  xxss ssss
        flag_bits = (data[0] >> 6) & 0x03
        flags = ChunkFlags()
        flags.resend = (flag_bits & CHUNKFLAG7_RESEND) != 0
        flags.vital = (flag_bits & CHUNKFLAG7_VITAL) != 0
        return flags

    # the first byte of data has to be the
    # first byte of the chunk header
    def parse_header7(self, data: bytes) -> ChunkHeader:
        header = ChunkHeader()
        header.flags = self.parse_flags7(data)
        # ffSS SSSS  xxSS SSSS
        header.size = ((data[0] & 0x3F) << 6) | (data[1] & 0x3F)
        if header.flags.vital:
            # ffss ssss  XXss ssss
            header.seq = ((data[1] & 0xC0) << 2) | data[2]
        return header

class PacketParser():
    def __init__(self) -> None:
        self.version: Literal['0.6', '0.7'] = '0.7'

    # the first byte of data has to be the
    # first byte of a message chunk
    # NOT the whole packet with packet header
    def get_messages(self, data: bytes) -> list[NetMessage]:
        messages: list[NetMessage] = []
        i = 0
        while i < len(data):
            msg = self.get_message(data[i:])
            if msg.header.size is None:
                raise ValueError('header size is not set')
            i += msg.header.size + 2 # header + msg id = 3
            if msg.header.flags.vital:
                i += 1
            messages.append(msg)
        return messages

    # the first byte of data has to be the
    # first byte of a message chunk
    # NOT the whole packet with packet header
    def get_message(self, data: bytes) -> NetMessage:
        chunk_header = ChunkHeaderParser().parse_header7(data)
        i = 2
        if chunk_header.flags.vital:
            i += 1
        unpacker = Unpacker(data[i:])
        msg_id: int = unpacker.get_int()
        i += 1
        sys: bool = (msg_id & 1) == 1
        msg_id >>= 1
        msg: NetMessage
        if sys:
            msg = MessageParser().parse_sys_message(self.version, msg_id, unpacker.get_raw())
        else:
            msg = MessageParser().parse_game_message(self.version, msg_id, unpacker.get_raw())
        msg.header = chunk_header
        return msg

    def parse6(self, data: bytes, client: bool) -> TwPacket:
        pck = TwPacket(version = '0.6')
        self.version = '0.6'
        # TODO: what is the most performant way in python to do this?
        #       heap allocating a PacketHeaderParser7 just to bundle a bunch of
        #       methods that do not share state seems like a waste of performance
        #       would this be nicer with class methods?
        pck.header = PacketHeaderParser6().parse_header(data)
        header_size = PACKET_HEADER7_SIZE
        if pck.header.flags.connless:
            header_size = CONNLESS_PACKET_HEADER6_SIZE
        elif not pck.header.flags.token:
            header_size = 3
        pck.payload_raw = data[header_size:]
        pck.payload_decompressed = pck.payload_raw
        if pck.header.flags.control:
            ctrl_msg: CtrlMessage = match_control6(data[header_size], data[header_size+1:], client)
            pck.messages.append(ctrl_msg)
            return pck
        if pck.header.flags.connless:
            connless_msg: ConnlessMessage = match_connless6(data[header_size:14], data[14:])
            pck.messages.append(connless_msg)
            return pck
        if pck.header.flags.compression:
            payload = bytearray(pck.payload_raw)
            pck.payload_decompressed = twnet_parser.huffman.decompress(payload)
        pck.messages = cast(
                list[Union[CtrlMessage, NetMessage, ConnlessMessage]],
                self.get_messages(pck.payload_decompressed))
        return pck

    def parse7(self, data: bytes, client: bool) -> TwPacket:
        pck = TwPacket(version = '0.7')
        self.version = '0.7'
        # TODO: what is the most performant way in python to do this?
        #       heap allocating a PacketHeaderParser7 just to bundle a bunch of
        #       methods that do not share state seems like a waste of performance
        #       would this be nicer with class methods?
        pck.header = PacketHeaderParser7().parse_header(data)
        header_size = PACKET_HEADER7_SIZE
        if pck.header.flags.connless:
            header_size = CONNLESS_PACKET_HEADER7_SIZE
        pck.payload_raw = data[header_size:]
        pck.payload_decompressed = pck.payload_raw
        if pck.header.flags.control:
            ctrl_msg: CtrlMessage = match_control7(data[header_size], data[8:], client)
            pck.messages.append(ctrl_msg)
            return pck
        if pck.header.flags.connless:
            connless_msg: ConnlessMessage = match_connless7(data[header_size:17], data[17:])
            pck.messages.append(connless_msg)
            return pck
        if pck.header.flags.compression:
            payload = bytearray(pck.payload_raw)
            pck.payload_decompressed = twnet_parser.huffman.decompress(payload)
        pck.messages = cast(
                list[Union[CtrlMessage, NetMessage, ConnlessMessage]],
                self.get_messages(pck.payload_decompressed))
        return pck

def parse6(data: bytes, we_are_a_client: bool = True) -> TwPacket:
    return PacketParser().parse6(data, we_are_a_client)

def parse7(data: bytes, we_are_a_client: bool = True) -> TwPacket:
    return PacketParser().parse7(data, we_are_a_client)
