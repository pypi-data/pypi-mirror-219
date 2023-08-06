
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n sentinel/mint/v1/inflation.proto\x12\x10sentinel.mint.v1\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xc9\x02\n\tInflation\x12I\n\x03max\x18\x01 \x01(\tB<\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\nyaml:"max"\xc8\xde\x1f\x00\x12I\n\x03min\x18\x02 \x01(\tB<\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\nyaml:"min"\xc8\xde\x1f\x00\x12Y\n\x0brate_change\x18\x03 \x01(\tBD\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x12yaml:"rate_change"\xc8\xde\x1f\x00\x12K\n\ttimestamp\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1c\xf2\xde\x1f\x10yaml:"timestamp"\xc8\xde\x1f\x00\x90\xdf\x1f\x01B7Z-github.com/sentinel-official/hub/x/mint/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.mint.v1.inflation_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/mint/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _INFLATION.fields_by_name['max']._options = None
    _INFLATION.fields_by_name['max']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\nyaml:"max"\xc8\xde\x1f\x00'
    _INFLATION.fields_by_name['min']._options = None
    _INFLATION.fields_by_name['min']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\nyaml:"min"\xc8\xde\x1f\x00'
    _INFLATION.fields_by_name['rate_change']._options = None
    _INFLATION.fields_by_name['rate_change']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x12yaml:"rate_change"\xc8\xde\x1f\x00'
    _INFLATION.fields_by_name['timestamp']._options = None
    _INFLATION.fields_by_name['timestamp']._serialized_options = b'\xf2\xde\x1f\x10yaml:"timestamp"\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _INFLATION._serialized_start = 110
    _INFLATION._serialized_end = 439
