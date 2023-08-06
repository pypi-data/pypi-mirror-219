
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$sentinel/subscription/v1/quota.proto\x12\x18sentinel.subscription.v1\x1a\x14gogoproto/gogo.proto"\x9d\x01\n\x05Quota\x12\x0f\n\x07address\x18\x01 \x01(\t\x12A\n\tallocated\x18\x02 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00\x12@\n\x08consumed\x18\x03 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00BIZ?github.com/sentinel-official/hub/x/subscription/legacy/v1/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.subscription.v1.quota_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z?github.com/sentinel-official/hub/x/subscription/legacy/v1/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _QUOTA.fields_by_name['allocated']._options = None
    _QUOTA.fields_by_name['allocated']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00'
    _QUOTA.fields_by_name['consumed']._options = None
    _QUOTA.fields_by_name['consumed']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00'
    _QUOTA._serialized_start = 89
    _QUOTA._serialized_end = 246
