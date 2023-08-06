
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.provider.v2 import params_pb2 as sentinel_dot_provider_dot_v2_dot_params__pb2
from ....sentinel.provider.v2 import provider_pb2 as sentinel_dot_provider_dot_v2_dot_provider__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"sentinel/provider/v2/genesis.proto\x12\x14sentinel.provider.v2\x1a\x14gogoproto/gogo.proto\x1a!sentinel/provider/v2/params.proto\x1a#sentinel/provider/v2/provider.proto"{\n\x0cGenesisState\x127\n\tproviders\x18\x01 \x03(\x0b2\x1e.sentinel.provider.v2.ProviderB\x04\xc8\xde\x1f\x00\x122\n\x06params\x18\x02 \x01(\x0b2\x1c.sentinel.provider.v2.ParamsB\x04\xc8\xde\x1f\x00B;Z1github.com/sentinel-official/hub/x/provider/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.provider.v2.genesis_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z1github.com/sentinel-official/hub/x/provider/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _GENESISSTATE.fields_by_name['providers']._options = None
    _GENESISSTATE.fields_by_name['providers']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE._serialized_start = 154
    _GENESISSTATE._serialized_end = 277
