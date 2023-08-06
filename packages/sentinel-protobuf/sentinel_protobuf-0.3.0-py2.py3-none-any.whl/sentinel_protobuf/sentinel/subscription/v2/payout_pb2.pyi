
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Payout(_message.Message):
    __slots__ = ['address', 'hours', 'id', 'node_address', 'price', 'timestamp']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    HOURS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    address: str
    hours: int
    id: int
    node_address: str
    price: _coin_pb2.Coin
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, id: _Optional[int]=..., address: _Optional[str]=..., node_address: _Optional[str]=..., hours: _Optional[int]=..., price: _Optional[_Union[(_coin_pb2.Coin, _Mapping)]]=..., timestamp: _Optional[_Union[(_timestamp_pb2.Timestamp, _Mapping)]]=...) -> None:
        ...
