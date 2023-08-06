
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Plan(_message.Message):
    __slots__ = ['address', 'duration', 'gigabytes', 'id', 'prices', 'status', 'status_at']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    GIGABYTES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRICES_FIELD_NUMBER: _ClassVar[int]
    STATUS_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    address: str
    duration: _duration_pb2.Duration
    gigabytes: int
    id: int
    prices: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    status: _status_pb2.Status
    status_at: _timestamp_pb2.Timestamp

    def __init__(self, id: _Optional[int]=..., address: _Optional[str]=..., duration: _Optional[_Union[(_duration_pb2.Duration, _Mapping)]]=..., gigabytes: _Optional[int]=..., prices: _Optional[_Iterable[_Union[(_coin_pb2.Coin, _Mapping)]]]=..., status: _Optional[_Union[(_status_pb2.Status, str)]]=..., status_at: _Optional[_Union[(_timestamp_pb2.Timestamp, _Mapping)]]=...) -> None:
        ...
