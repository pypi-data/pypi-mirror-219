from typing import Literal, Optional

from twnet_parser.pretty_print import PrettyPrint
from twnet_parser.packer import Unpacker
from twnet_parser.chunk_header import ChunkHeader
from twnet_parser.packer import pack_int
from twnet_parser.snapshot7 import Snapshot

class MsgSnap(PrettyPrint):
    def __init__(
            self,
            chunk_header: ChunkHeader = ChunkHeader(),
            tick: int = 0,
            delta_tick: int = 0,
            num_parts: int = 0,
            part: int = 0,
            crc: int = 0,
            data_size: Optional[int] = None,
            data: bytes = b'\x00'
    ) -> None:
        self.message_type: Literal['system', 'game'] = 'system'
        self.message_name: str = 'snap'
        self.system_message: bool = True
        self.message_id: int = 6
        self.header: ChunkHeader = chunk_header

        self.tick: int = tick
        self.delta_tick: int = delta_tick
        self.num_parts: int = num_parts
        self.part: int = part
        self.crc: int = crc
        self.data_size: int = data_size if data_size else len(data)
        self.data: bytes = data
        self.snapshot = Snapshot()

    # first byte of data
    # has to be the first byte of the message payload
    # NOT the chunk header and NOT the message id
    def unpack(self, data: bytes) -> bool:
        unpacker = Unpacker(data)
        self.tick = unpacker.get_int()
        self.delta_tick = unpacker.get_int()
        self.num_parts = unpacker.get_int()
        self.part = unpacker.get_int()
        self.crc = unpacker.get_int()
        self.data_size = unpacker.get_int()
        self.data = unpacker.get_raw(self.data_size)
        self.snapshot.unpack(self.data)
        return True

    def pack(self) -> bytes:
        return pack_int(self.tick) + \
            pack_int(self.delta_tick) + \
            pack_int(self.num_parts) + \
            pack_int(self.part) + \
            pack_int(self.crc) + \
            pack_int(self.data_size) + \
            self.snapshot.pack()
