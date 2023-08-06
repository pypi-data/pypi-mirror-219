
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.plan.v2 import plan_pb2 as sentinel_dot_plan_dot_v2_dot_plan__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1esentinel/plan/v2/genesis.proto\x12\x10sentinel.plan.v2\x1a\x14gogoproto/gogo.proto\x1a\x1bsentinel/plan/v2/plan.proto"H\n\x0bGenesisPlan\x12*\n\x04plan\x18\x01 \x01(\x0b2\x16.sentinel.plan.v2.PlanB\x04\xc8\xde\x1f\x00\x12\r\n\x05nodes\x18\x02 \x03(\tB7Z-github.com/sentinel-official/hub/x/plan/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.plan.v2.genesis_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/plan/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _GENESISPLAN.fields_by_name['plan']._options = None
    _GENESISPLAN.fields_by_name['plan']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISPLAN._serialized_start = 103
    _GENESISPLAN._serialized_end = 175
