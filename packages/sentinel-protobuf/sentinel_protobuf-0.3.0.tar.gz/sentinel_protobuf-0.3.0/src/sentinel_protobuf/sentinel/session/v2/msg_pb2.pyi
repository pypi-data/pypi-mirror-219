
from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.session.v2 import proof_pb2 as _proof_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgEndRequest(_message.Message):
    __slots__ = ['frm', 'id', 'rating']
    FRM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    frm: str
    id: int
    rating: int

    def __init__(self, frm: _Optional[str]=..., id: _Optional[int]=..., rating: _Optional[int]=...) -> None:
        ...

class MsgEndResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgStartRequest(_message.Message):
    __slots__ = ['address', 'frm', 'id']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FRM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    frm: str
    id: int

    def __init__(self, frm: _Optional[str]=..., id: _Optional[int]=..., address: _Optional[str]=...) -> None:
        ...

class MsgStartResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgUpdateDetailsRequest(_message.Message):
    __slots__ = ['frm', 'proof', 'signature']
    FRM_FIELD_NUMBER: _ClassVar[int]
    PROOF_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    frm: str
    proof: _proof_pb2.Proof
    signature: bytes

    def __init__(self, frm: _Optional[str]=..., proof: _Optional[_Union[(_proof_pb2.Proof, _Mapping)]]=..., signature: _Optional[bytes]=...) -> None:
        ...

class MsgUpdateDetailsResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...
