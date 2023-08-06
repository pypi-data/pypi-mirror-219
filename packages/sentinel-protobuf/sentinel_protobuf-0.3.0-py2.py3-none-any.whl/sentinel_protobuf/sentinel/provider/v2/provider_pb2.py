
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#sentinel/provider/v2/provider.proto\x12\x14sentinel.provider.v2\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1esentinel/types/v1/status.proto"\xc5\x01\n\x08Provider\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08identity\x18\x03 \x01(\t\x12\x0f\n\x07website\x18\x04 \x01(\t\x12\x13\n\x0bdescription\x18\x05 \x01(\t\x12)\n\x06status\x18\x06 \x01(\x0e2\x19.sentinel.types.v1.Status\x127\n\tstatus_at\x18\x07 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01B;Z1github.com/sentinel-official/hub/x/provider/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.provider.v2.provider_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z1github.com/sentinel-official/hub/x/provider/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _PROVIDER.fields_by_name['status_at']._options = None
    _PROVIDER.fields_by_name['status_at']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _PROVIDER._serialized_start = 149
    _PROVIDER._serialized_end = 346
