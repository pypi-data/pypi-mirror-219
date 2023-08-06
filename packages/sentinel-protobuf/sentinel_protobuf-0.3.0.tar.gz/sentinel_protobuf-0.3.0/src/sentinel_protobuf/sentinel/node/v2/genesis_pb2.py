
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.node.v2 import node_pb2 as sentinel_dot_node_dot_v2_dot_node__pb2
from ....sentinel.node.v2 import params_pb2 as sentinel_dot_node_dot_v2_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1esentinel/node/v2/genesis.proto\x12\x10sentinel.node.v2\x1a\x14gogoproto/gogo.proto\x1a\x1bsentinel/node/v2/node.proto\x1a\x1dsentinel/node/v2/params.proto"k\n\x0cGenesisState\x12+\n\x05nodes\x18\x01 \x03(\x0b2\x16.sentinel.node.v2.NodeB\x04\xc8\xde\x1f\x00\x12.\n\x06params\x18\x02 \x01(\x0b2\x18.sentinel.node.v2.ParamsB\x04\xc8\xde\x1f\x00B7Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.node.v2.genesis_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _GENESISSTATE.fields_by_name['nodes']._options = None
    _GENESISSTATE.fields_by_name['nodes']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE._serialized_start = 134
    _GENESISSTATE._serialized_end = 241
