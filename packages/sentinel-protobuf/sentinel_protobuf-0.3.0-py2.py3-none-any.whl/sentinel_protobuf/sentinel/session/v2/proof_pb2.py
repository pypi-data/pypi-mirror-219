
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ....sentinel.types.v1 import bandwidth_pb2 as sentinel_dot_types_dot_v1_dot_bandwidth__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fsentinel/session/v2/proof.proto\x12\x13sentinel.session.v2\x1a\x14gogoproto/gogo.proto\x1a\x1egoogle/protobuf/duration.proto\x1a!sentinel/types/v1/bandwidth.proto"\x89\x01\n\x05Proof\x12\x12\n\x02id\x18\x01 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x125\n\tbandwidth\x18\x02 \x01(\x0b2\x1c.sentinel.types.v1.BandwidthB\x04\xc8\xde\x1f\x00\x125\n\x08duration\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationB\x08\x98\xdf\x1f\x01\xc8\xde\x1f\x00B:Z0github.com/sentinel-official/hub/x/session/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.session.v2.proof_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/sentinel-official/hub/x/session/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _PROOF.fields_by_name['id']._options = None
    _PROOF.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _PROOF.fields_by_name['bandwidth']._options = None
    _PROOF.fields_by_name['bandwidth']._serialized_options = b'\xc8\xde\x1f\x00'
    _PROOF.fields_by_name['duration']._options = None
    _PROOF.fields_by_name['duration']._serialized_options = b'\x98\xdf\x1f\x01\xc8\xde\x1f\x00'
    _PROOF._serialized_start = 146
    _PROOF._serialized_end = 283
