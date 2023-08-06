
from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class EventAllocate(_message.Message):
    __slots__ = ['address', 'bytes', 'id']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    bytes: str
    id: int

    def __init__(self, id: _Optional[int]=..., address: _Optional[str]=..., bytes: _Optional[str]=...) -> None:
        ...

class EventPayout(_message.Message):
    __slots__ = ['address', 'id', 'node_address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    node_address: str

    def __init__(self, id: _Optional[int]=..., address: _Optional[str]=..., node_address: _Optional[str]=...) -> None:
        ...

class EventUpdateStatus(_message.Message):
    __slots__ = ['id', 'status']
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    status: _status_pb2.Status

    def __init__(self, id: _Optional[int]=..., status: _Optional[_Union[(_status_pb2.Status, str)]]=...) -> None:
        ...
