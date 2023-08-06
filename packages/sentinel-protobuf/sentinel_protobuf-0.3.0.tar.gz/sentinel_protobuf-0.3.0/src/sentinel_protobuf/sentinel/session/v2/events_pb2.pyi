
from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class EventStart(_message.Message):
    __slots__ = ['id', 'node_address', 'subscription_id']
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    node_address: str
    subscription_id: int

    def __init__(self, id: _Optional[int]=..., subscription_id: _Optional[int]=..., node_address: _Optional[str]=...) -> None:
        ...

class EventUpdateDetails(_message.Message):
    __slots__ = ['id', 'node_address', 'subscription_id']
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    node_address: str
    subscription_id: int

    def __init__(self, id: _Optional[int]=..., subscription_id: _Optional[int]=..., node_address: _Optional[str]=...) -> None:
        ...

class EventUpdateStatus(_message.Message):
    __slots__ = ['id', 'node_address', 'status', 'subscription_id']
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    node_address: str
    status: _status_pb2.Status
    subscription_id: int

    def __init__(self, id: _Optional[int]=..., subscription_id: _Optional[int]=..., node_address: _Optional[str]=..., status: _Optional[_Union[(_status_pb2.Status, str)]]=...) -> None:
        ...
