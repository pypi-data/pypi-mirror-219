from typing import Literal
from twnet_parser.pretty_print import PrettyPrint

class CtrlKeepAlive(PrettyPrint):
    def __init__(self) -> None:
        self.message_type: Literal['control'] = 'control'
        self.message_name: str = 'keep_alive'
        self.message_id: int = 0

    def unpack(self, data: bytes, we_are_a_client: bool = True) -> bool:
        return False

    def pack(self, we_are_a_client: bool = True) -> bytes:
        return b''
