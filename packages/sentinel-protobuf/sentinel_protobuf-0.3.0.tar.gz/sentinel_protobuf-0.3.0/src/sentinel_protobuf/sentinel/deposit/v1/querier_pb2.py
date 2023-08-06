
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....sentinel.deposit.v1 import deposit_pb2 as sentinel_dot_deposit_dot_v1_dot_deposit__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!sentinel/deposit/v1/querier.proto\x12\x13sentinel.deposit.v1\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a!sentinel/deposit/v1/deposit.proto"R\n\x14QueryDepositsRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"&\n\x13QueryDepositRequest\x12\x0f\n\x07address\x18\x01 \x01(\t"\x8a\x01\n\x15QueryDepositsResponse\x124\n\x08deposits\x18\x01 \x03(\x0b2\x1c.sentinel.deposit.v1.DepositB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"K\n\x14QueryDepositResponse\x123\n\x07deposit\x18\x01 \x01(\x0b2\x1c.sentinel.deposit.v1.DepositB\x04\xc8\xde\x1f\x002\x9f\x02\n\x0cQueryService\x12\x82\x01\n\rQueryDeposits\x12).sentinel.deposit.v1.QueryDepositsRequest\x1a*.sentinel.deposit.v1.QueryDepositsResponse"\x1a\x82\xd3\xe4\x93\x02\x14\x12\x12/sentinel/deposits\x12\x89\x01\n\x0cQueryDeposit\x12(.sentinel.deposit.v1.QueryDepositRequest\x1a).sentinel.deposit.v1.QueryDepositResponse"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/sentinel/deposits/{address}B:Z0github.com/sentinel-official/hub/x/deposit/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.deposit.v1.querier_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/sentinel-official/hub/x/deposit/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _QUERYDEPOSITSRESPONSE.fields_by_name['deposits']._options = None
    _QUERYDEPOSITSRESPONSE.fields_by_name['deposits']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYDEPOSITRESPONSE.fields_by_name['deposit']._options = None
    _QUERYDEPOSITRESPONSE.fields_by_name['deposit']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSERVICE.methods_by_name['QueryDeposits']._options = None
    _QUERYSERVICE.methods_by_name['QueryDeposits']._serialized_options = b'\x82\xd3\xe4\x93\x02\x14\x12\x12/sentinel/deposits'
    _QUERYSERVICE.methods_by_name['QueryDeposit']._options = None
    _QUERYSERVICE.methods_by_name['QueryDeposit']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1e\x12\x1c/sentinel/deposits/{address}'
    _QUERYDEPOSITSREQUEST._serialized_start = 189
    _QUERYDEPOSITSREQUEST._serialized_end = 271
    _QUERYDEPOSITREQUEST._serialized_start = 273
    _QUERYDEPOSITREQUEST._serialized_end = 311
    _QUERYDEPOSITSRESPONSE._serialized_start = 314
    _QUERYDEPOSITSRESPONSE._serialized_end = 452
    _QUERYDEPOSITRESPONSE._serialized_start = 454
    _QUERYDEPOSITRESPONSE._serialized_end = 529
    _QUERYSERVICE._serialized_start = 532
    _QUERYSERVICE._serialized_end = 819
