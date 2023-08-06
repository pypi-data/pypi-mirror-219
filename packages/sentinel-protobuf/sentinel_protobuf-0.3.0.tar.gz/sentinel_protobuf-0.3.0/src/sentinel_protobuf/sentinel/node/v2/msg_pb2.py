
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1asentinel/node/v2/msg.proto\x12\x10sentinel.node.v2\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x1esentinel/types/v1/status.proto"\x8e\x02\n\x12MsgRegisterRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12d\n\x0fgigabyte_prices\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12b\n\rhourly_prices\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12!\n\nremote_url\x18\x04 \x01(\tB\r\xe2\xde\x1f\tRemoteURL"\x93\x02\n\x17MsgUpdateDetailsRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12d\n\x0fgigabyte_prices\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12b\n\rhourly_prices\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12!\n\nremote_url\x18\x04 \x01(\tB\r\xe2\xde\x1f\tRemoteURL"P\n\x16MsgUpdateStatusRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12)\n\x06status\x18\x02 \x01(\x0e2\x19.sentinel.types.v1.Status"d\n\x13MsgSubscribeRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12\x0f\n\x07address\x18\x02 \x01(\t\x12\x11\n\tgigabytes\x18\x03 \x01(\x03\x12\r\n\x05hours\x18\x04 \x01(\x03\x12\r\n\x05denom\x18\x05 \x01(\t"\x15\n\x13MsgRegisterResponse"\x1a\n\x18MsgUpdateDetailsResponse"\x19\n\x17MsgUpdateStatusResponse"\x16\n\x14MsgSubscribeResponse2\x9a\x03\n\nMsgService\x12Z\n\x0bMsgRegister\x12$.sentinel.node.v2.MsgRegisterRequest\x1a%.sentinel.node.v2.MsgRegisterResponse\x12i\n\x10MsgUpdateDetails\x12).sentinel.node.v2.MsgUpdateDetailsRequest\x1a*.sentinel.node.v2.MsgUpdateDetailsResponse\x12f\n\x0fMsgUpdateStatus\x12(.sentinel.node.v2.MsgUpdateStatusRequest\x1a).sentinel.node.v2.MsgUpdateStatusResponse\x12]\n\x0cMsgSubscribe\x12%.sentinel.node.v2.MsgSubscribeRequest\x1a&.sentinel.node.v2.MsgSubscribeResponseB7Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.node.v2.msg_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _MSGREGISTERREQUEST.fields_by_name['gigabyte_prices']._options = None
    _MSGREGISTERREQUEST.fields_by_name['gigabyte_prices']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGREGISTERREQUEST.fields_by_name['hourly_prices']._options = None
    _MSGREGISTERREQUEST.fields_by_name['hourly_prices']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGREGISTERREQUEST.fields_by_name['remote_url']._options = None
    _MSGREGISTERREQUEST.fields_by_name['remote_url']._serialized_options = b'\xe2\xde\x1f\tRemoteURL'
    _MSGUPDATEDETAILSREQUEST.fields_by_name['gigabyte_prices']._options = None
    _MSGUPDATEDETAILSREQUEST.fields_by_name['gigabyte_prices']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGUPDATEDETAILSREQUEST.fields_by_name['hourly_prices']._options = None
    _MSGUPDATEDETAILSREQUEST.fields_by_name['hourly_prices']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGUPDATEDETAILSREQUEST.fields_by_name['remote_url']._options = None
    _MSGUPDATEDETAILSREQUEST.fields_by_name['remote_url']._serialized_options = b'\xe2\xde\x1f\tRemoteURL'
    _MSGREGISTERREQUEST._serialized_start = 135
    _MSGREGISTERREQUEST._serialized_end = 405
    _MSGUPDATEDETAILSREQUEST._serialized_start = 408
    _MSGUPDATEDETAILSREQUEST._serialized_end = 683
    _MSGUPDATESTATUSREQUEST._serialized_start = 685
    _MSGUPDATESTATUSREQUEST._serialized_end = 765
    _MSGSUBSCRIBEREQUEST._serialized_start = 767
    _MSGSUBSCRIBEREQUEST._serialized_end = 867
    _MSGREGISTERRESPONSE._serialized_start = 869
    _MSGREGISTERRESPONSE._serialized_end = 890
    _MSGUPDATEDETAILSRESPONSE._serialized_start = 892
    _MSGUPDATEDETAILSRESPONSE._serialized_end = 918
    _MSGUPDATESTATUSRESPONSE._serialized_start = 920
    _MSGUPDATESTATUSRESPONSE._serialized_end = 945
    _MSGSUBSCRIBERESPONSE._serialized_start = 947
    _MSGSUBSCRIBERESPONSE._serialized_end = 969
    _MSGSERVICE._serialized_start = 972
    _MSGSERVICE._serialized_end = 1382
