from twnet_parser.packer import Unpacker

class Snapshot:
    def __init__(
            self,
            num_removed_items: int = 0,
            num_item_deltas: int = 0
    ) -> None:
        self.num_removed_items: int = num_removed_items
        self.num_item_deltas: int = num_item_deltas

    # expects the int compressed
    # data field of the snap message
    # not the whole snap message with crc
    # and the other fields
    def unpack(self, data: bytes) -> bool:
        unpacker = Unpacker(data)
        self.num_removed_items = unpacker.get_int()
        self.num_item_deltas = unpacker.get_int()
        unpacker.get_int() # unused by tw 0.7 NumTempItems
        return True

    def pack(self) -> bytes:
        return b''

