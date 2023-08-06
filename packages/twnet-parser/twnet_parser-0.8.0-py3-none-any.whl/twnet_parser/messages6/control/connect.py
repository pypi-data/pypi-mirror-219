from typing import Literal
from twnet_parser.pretty_print import PrettyPrint

"""
CtrlConnect

with security token from 0.6.5
not compatible with 0.6.4 or earlier
also not compatible with 0.7 or later
"""
class CtrlConnect(PrettyPrint):
    def __init__(
            self,
            response_token: bytes = b'\xff\xff\xff\xff'
    ) -> None:
        self.message_type: Literal['control'] = 'control'
        self.message_name: str = 'connect'
        self.message_id: int = 1

        self.response_token: bytes = response_token

    def unpack(self, data: bytes, we_are_a_client: bool = True) -> bool:
        # anti reflection attack
        if len(data) < 512:
            return False
        self.response_token = data[4:8]
        return True

    def pack(self, we_are_a_client: bool = True) -> bytes:
        return bytes(4) + self.response_token + bytes(504)
