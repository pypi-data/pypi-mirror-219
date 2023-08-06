
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class MsgAllocateRequest(_message.Message):
    __slots__ = ['address', 'bytes', 'frm', 'id']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    FRM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    bytes: str
    frm: str
    id: int

    def __init__(self, frm: _Optional[str]=..., id: _Optional[int]=..., address: _Optional[str]=..., bytes: _Optional[str]=...) -> None:
        ...

class MsgAllocateResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgCancelRequest(_message.Message):
    __slots__ = ['frm', 'id']
    FRM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    frm: str
    id: int

    def __init__(self, frm: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...

class MsgCancelResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...
