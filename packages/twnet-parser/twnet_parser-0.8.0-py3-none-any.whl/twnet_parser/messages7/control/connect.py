from typing import Literal
from twnet_parser.pretty_print import PrettyPrint

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
        self.response_token = data[0:4]
        return True

    def pack(self, we_are_a_client: bool = True) -> bytes:
        return self.response_token + bytes(508)
