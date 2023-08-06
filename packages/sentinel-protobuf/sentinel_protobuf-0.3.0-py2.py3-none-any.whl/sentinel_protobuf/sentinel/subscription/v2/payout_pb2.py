
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%sentinel/subscription/v2/payout.proto\x12\x18sentinel.subscription.v2\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xbb\x01\n\x06Payout\x12\x12\n\x02id\x18\x01 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x12\x0f\n\x07address\x18\x02 \x01(\t\x12\x14\n\x0cnode_address\x18\x03 \x01(\t\x12\r\n\x05hours\x18\x04 \x01(\x03\x12.\n\x05price\x18\x05 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x127\n\ttimestamp\x18\x06 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01B?Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.subscription.v2.payout_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _PAYOUT.fields_by_name['id']._options = None
    _PAYOUT.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _PAYOUT.fields_by_name['price']._options = None
    _PAYOUT.fields_by_name['price']._serialized_options = b'\xc8\xde\x1f\x00'
    _PAYOUT.fields_by_name['timestamp']._options = None
    _PAYOUT.fields_by_name['timestamp']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _PAYOUT._serialized_start = 155
    _PAYOUT._serialized_end = 342
