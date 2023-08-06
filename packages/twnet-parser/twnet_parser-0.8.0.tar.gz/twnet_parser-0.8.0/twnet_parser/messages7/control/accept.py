from typing import Literal
from twnet_parser.pretty_print import PrettyPrint

class CtrlAccept(PrettyPrint):
    def __init__(self) -> None:
        self.message_type: Literal['control'] = 'control'
        self.message_name: str = 'accept'
        self.message_id: int = 2

    def unpack(self, data: bytes, we_are_a_client: bool = True) -> bool:
        return False

    def pack(self, we_are_a_client: bool = True) -> bytes:
        return b''
