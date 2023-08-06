from typing import Protocol, Literal, Annotated

class ConnlessMessage(Protocol):
    message_type: Literal['connless']
    message_name: str
    message_id: Annotated[list[int], 8]
    def unpack(self, data: bytes) -> bool:
        ...
    def pack(self) -> bytes:
        ...
