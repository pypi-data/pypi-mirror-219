
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bsentinel/node/v2/node.proto\x12\x10sentinel.node.v2\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1esentinel/types/v1/status.proto"\xa3\x03\n\x04Node\x12\x0f\n\x07address\x18\x01 \x01(\t\x12d\n\x0fgigabyte_prices\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12b\n\rhourly_prices\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12!\n\nremote_url\x18\x04 \x01(\tB\r\xe2\xde\x1f\tRemoteURL\x129\n\x0binactive_at\x18\x05 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12)\n\x06status\x18\x06 \x01(\x0e2\x19.sentinel.types.v1.Status\x127\n\tstatus_at\x18\x07 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01B7Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.node.v2.node_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _NODE.fields_by_name['gigabyte_prices']._options = None
    _NODE.fields_by_name['gigabyte_prices']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _NODE.fields_by_name['hourly_prices']._options = None
    _NODE.fields_by_name['hourly_prices']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _NODE.fields_by_name['remote_url']._options = None
    _NODE.fields_by_name['remote_url']._serialized_options = b'\xe2\xde\x1f\tRemoteURL'
    _NODE.fields_by_name['inactive_at']._options = None
    _NODE.fields_by_name['inactive_at']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _NODE.fields_by_name['status_at']._options = None
    _NODE.fields_by_name['status_at']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _NODE._serialized_start = 169
    _NODE._serialized_end = 588
