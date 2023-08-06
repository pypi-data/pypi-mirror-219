from typing import Protocol, Literal

class CtrlMessage(Protocol):
    message_type: Literal['control']
    message_name: str
    message_id: int
    def unpack(self, data: bytes, we_are_a_client: bool = True) -> bool:
        ...
    def pack(self, we_are_a_client: bool = True) -> bytes:
        ...
