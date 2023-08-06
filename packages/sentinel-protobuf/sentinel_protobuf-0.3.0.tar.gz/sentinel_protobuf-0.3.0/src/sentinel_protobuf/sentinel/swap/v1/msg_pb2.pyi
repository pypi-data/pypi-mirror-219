
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class MsgSwapRequest(_message.Message):
    __slots__ = ['amount', 'frm', 'receiver', 'tx_hash']
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    FRM_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_FIELD_NUMBER: _ClassVar[int]
    TX_HASH_FIELD_NUMBER: _ClassVar[int]
    amount: str
    frm: str
    receiver: str
    tx_hash: bytes

    def __init__(self, frm: _Optional[str]=..., tx_hash: _Optional[bytes]=..., receiver: _Optional[str]=..., amount: _Optional[str]=...) -> None:
        ...

class MsgSwapResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...
