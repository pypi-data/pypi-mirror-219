
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1asentinel/plan/v2/msg.proto\x12\x10sentinel.plan.v2\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x14gogoproto/gogo.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1esentinel/types/v1/status.proto"\xc6\x01\n\x10MsgCreateRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x125\n\x08duration\x18\x02 \x01(\x0b2\x19.google.protobuf.DurationB\x08\x98\xdf\x1f\x01\xc8\xde\x1f\x00\x12\x11\n\tgigabytes\x18\x03 \x01(\x03\x12[\n\x06prices\x18\x04 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins"d\n\x16MsgUpdateStatusRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12\x12\n\x02id\x18\x02 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x12)\n\x06status\x18\x03 \x01(\x0e2\x19.sentinel.types.v1.Status"F\n\x12MsgLinkNodeRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12\x12\n\x02id\x18\x02 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x12\x0f\n\x07address\x18\x03 \x01(\t"H\n\x14MsgUnlinkNodeRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12\x12\n\x02id\x18\x02 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x12\x0f\n\x07address\x18\x03 \x01(\t"E\n\x13MsgSubscribeRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12\x12\n\x02id\x18\x02 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x12\r\n\x05denom\x18\x03 \x01(\t"\x13\n\x11MsgCreateResponse"\x19\n\x17MsgUpdateStatusResponse"\x15\n\x13MsgLinkNodeResponse"\x17\n\x15MsgUnlinkNodeResponse"\x16\n\x14MsgSubscribeResponse2\xe7\x03\n\nMsgService\x12T\n\tMsgCreate\x12".sentinel.plan.v2.MsgCreateRequest\x1a#.sentinel.plan.v2.MsgCreateResponse\x12f\n\x0fMsgUpdateStatus\x12(.sentinel.plan.v2.MsgUpdateStatusRequest\x1a).sentinel.plan.v2.MsgUpdateStatusResponse\x12Z\n\x0bMsgLinkNode\x12$.sentinel.plan.v2.MsgLinkNodeRequest\x1a%.sentinel.plan.v2.MsgLinkNodeResponse\x12`\n\rMsgUnlinkNode\x12&.sentinel.plan.v2.MsgUnlinkNodeRequest\x1a\'.sentinel.plan.v2.MsgUnlinkNodeResponse\x12]\n\x0cMsgSubscribe\x12%.sentinel.plan.v2.MsgSubscribeRequest\x1a&.sentinel.plan.v2.MsgSubscribeResponseB7Z-github.com/sentinel-official/hub/x/plan/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.plan.v2.msg_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/plan/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _MSGCREATEREQUEST.fields_by_name['duration']._options = None
    _MSGCREATEREQUEST.fields_by_name['duration']._serialized_options = b'\x98\xdf\x1f\x01\xc8\xde\x1f\x00'
    _MSGCREATEREQUEST.fields_by_name['prices']._options = None
    _MSGCREATEREQUEST.fields_by_name['prices']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGUPDATESTATUSREQUEST.fields_by_name['id']._options = None
    _MSGUPDATESTATUSREQUEST.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _MSGLINKNODEREQUEST.fields_by_name['id']._options = None
    _MSGLINKNODEREQUEST.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _MSGUNLINKNODEREQUEST.fields_by_name['id']._options = None
    _MSGUNLINKNODEREQUEST.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _MSGSUBSCRIBEREQUEST.fields_by_name['id']._options = None
    _MSGSUBSCRIBEREQUEST.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _MSGCREATEREQUEST._serialized_start = 167
    _MSGCREATEREQUEST._serialized_end = 365
    _MSGUPDATESTATUSREQUEST._serialized_start = 367
    _MSGUPDATESTATUSREQUEST._serialized_end = 467
    _MSGLINKNODEREQUEST._serialized_start = 469
    _MSGLINKNODEREQUEST._serialized_end = 539
    _MSGUNLINKNODEREQUEST._serialized_start = 541
    _MSGUNLINKNODEREQUEST._serialized_end = 613
    _MSGSUBSCRIBEREQUEST._serialized_start = 615
    _MSGSUBSCRIBEREQUEST._serialized_end = 684
    _MSGCREATERESPONSE._serialized_start = 686
    _MSGCREATERESPONSE._serialized_end = 705
    _MSGUPDATESTATUSRESPONSE._serialized_start = 707
    _MSGUPDATESTATUSRESPONSE._serialized_end = 732
    _MSGLINKNODERESPONSE._serialized_start = 734
    _MSGLINKNODERESPONSE._serialized_end = 755
    _MSGUNLINKNODERESPONSE._serialized_start = 757
    _MSGUNLINKNODERESPONSE._serialized_end = 780
    _MSGSUBSCRIBERESPONSE._serialized_start = 782
    _MSGSUBSCRIBERESPONSE._serialized_end = 804
    _MSGSERVICE._serialized_start = 807
    _MSGSERVICE._serialized_end = 1294
