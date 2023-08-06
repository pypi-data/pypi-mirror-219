
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!sentinel/types/v1/bandwidth.proto\x12\x11sentinel.types.v1\x1a\x14gogoproto/gogo.proto"\x8d\x01\n\tBandwidth\x12>\n\x06upload\x18\x01 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00\x12@\n\x08download\x18\x02 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00B0Z&github.com/sentinel-official/hub/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.types.v1.bandwidth_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z&github.com/sentinel-official/hub/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _BANDWIDTH.fields_by_name['upload']._options = None
    _BANDWIDTH.fields_by_name['upload']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00'
    _BANDWIDTH.fields_by_name['download']._options = None
    _BANDWIDTH.fields_by_name['download']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00'
    _BANDWIDTH._serialized_start = 79
    _BANDWIDTH._serialized_end = 220
