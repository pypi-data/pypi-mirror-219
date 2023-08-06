from typing import Literal
from twnet_parser.pretty_print import PrettyPrint

"""
CtrlConnectAccept

Only valid in 0.6.4 and earlier
got removed in 0.6.5
"""
class CtrlConnectAccept(PrettyPrint):
    def __init__(
            self,
            response_token: bytes = b'\xff\xff\xff\xff'
    ) -> None:
        self.message_type: Literal['control'] = 'control'
        self.message_name: str = 'connect_accept'
        self.message_id: int = 2

        self.response_token: bytes = response_token

    def unpack(self, data: bytes, we_are_a_client: bool = True) -> bool:
        self.response_token = data[0:4]
        return True

    def pack(self, we_are_a_client: bool = True) -> bytes:
        return self.response_token
