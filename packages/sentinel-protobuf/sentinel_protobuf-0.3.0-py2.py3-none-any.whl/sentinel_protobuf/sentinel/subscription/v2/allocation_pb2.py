
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)sentinel/subscription/v2/allocation.proto\x12\x18sentinel.subscription.v2\x1a\x14gogoproto/gogo.proto"\xc0\x01\n\nAllocation\x12\x12\n\x02id\x18\x01 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x12\x0f\n\x07address\x18\x02 \x01(\t\x12E\n\rgranted_bytes\x18\x03 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00\x12F\n\x0eutilised_bytes\x18\x04 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00B?Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.subscription.v2.allocation_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _ALLOCATION.fields_by_name['id']._options = None
    _ALLOCATION.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _ALLOCATION.fields_by_name['granted_bytes']._options = None
    _ALLOCATION.fields_by_name['granted_bytes']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00'
    _ALLOCATION.fields_by_name['utilised_bytes']._options = None
    _ALLOCATION.fields_by_name['utilised_bytes']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00'
    _ALLOCATION._serialized_start = 94
    _ALLOCATION._serialized_end = 286
