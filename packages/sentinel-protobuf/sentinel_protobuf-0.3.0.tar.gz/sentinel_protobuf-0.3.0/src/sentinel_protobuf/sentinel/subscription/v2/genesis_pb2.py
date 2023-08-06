
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....sentinel.subscription.v2 import allocation_pb2 as sentinel_dot_subscription_dot_v2_dot_allocation__pb2
from ....sentinel.subscription.v2 import params_pb2 as sentinel_dot_subscription_dot_v2_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&sentinel/subscription/v2/genesis.proto\x12\x18sentinel.subscription.v2\x1a\x14gogoproto/gogo.proto\x1a\x19google/protobuf/any.proto\x1a)sentinel/subscription/v2/allocation.proto\x1a%sentinel/subscription/v2/params.proto"\x82\x01\n\x13GenesisSubscription\x12*\n\x0csubscription\x18\x01 \x01(\x0b2\x14.google.protobuf.Any\x12?\n\x0ballocations\x18\x02 \x03(\x0b2$.sentinel.subscription.v2.AllocationB\x04\xc8\xde\x1f\x00"\x92\x01\n\x0cGenesisState\x12J\n\rsubscriptions\x18\x01 \x03(\x0b2-.sentinel.subscription.v2.GenesisSubscriptionB\x04\xc8\xde\x1f\x00\x126\n\x06params\x18\x02 \x01(\x0b2 .sentinel.subscription.v2.ParamsB\x04\xc8\xde\x1f\x00B?Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.subscription.v2.genesis_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _GENESISSUBSCRIPTION.fields_by_name['allocations']._options = None
    _GENESISSUBSCRIPTION.fields_by_name['allocations']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['subscriptions']._options = None
    _GENESISSTATE.fields_by_name['subscriptions']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSUBSCRIPTION._serialized_start = 200
    _GENESISSUBSCRIPTION._serialized_end = 330
    _GENESISSTATE._serialized_start = 333
    _GENESISSTATE._serialized_end = 479
