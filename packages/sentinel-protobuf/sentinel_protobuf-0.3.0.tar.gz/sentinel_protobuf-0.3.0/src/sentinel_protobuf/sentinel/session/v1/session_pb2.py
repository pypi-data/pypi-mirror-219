
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ....sentinel.types.v1 import bandwidth_pb2 as sentinel_dot_types_dot_v1_dot_bandwidth__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!sentinel/session/v1/session.proto\x12\x13sentinel.session.v1\x1a\x14gogoproto/gogo.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a!sentinel/types/v1/bandwidth.proto\x1a\x1esentinel/types/v1/status.proto"\x9c\x02\n\x07Session\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x14\n\x0csubscription\x18\x02 \x01(\x04\x12\x0c\n\x04node\x18\x03 \x01(\t\x12\x0f\n\x07address\x18\x04 \x01(\t\x125\n\x08duration\x18\x05 \x01(\x0b2\x19.google.protobuf.DurationB\x08\x98\xdf\x1f\x01\xc8\xde\x1f\x00\x125\n\tbandwidth\x18\x06 \x01(\x0b2\x1c.sentinel.types.v1.BandwidthB\x04\xc8\xde\x1f\x00\x12)\n\x06status\x18\x07 \x01(\x0e2\x19.sentinel.types.v1.Status\x127\n\tstatus_at\x18\x08 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01BDZ:github.com/sentinel-official/hub/x/session/legacy/v1/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.session.v1.session_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z:github.com/sentinel-official/hub/x/session/legacy/v1/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _SESSION.fields_by_name['duration']._options = None
    _SESSION.fields_by_name['duration']._serialized_options = b'\x98\xdf\x1f\x01\xc8\xde\x1f\x00'
    _SESSION.fields_by_name['bandwidth']._options = None
    _SESSION.fields_by_name['bandwidth']._serialized_options = b'\xc8\xde\x1f\x00'
    _SESSION.fields_by_name['status_at']._options = None
    _SESSION.fields_by_name['status_at']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _SESSION._serialized_start = 213
    _SESSION._serialized_end = 497
