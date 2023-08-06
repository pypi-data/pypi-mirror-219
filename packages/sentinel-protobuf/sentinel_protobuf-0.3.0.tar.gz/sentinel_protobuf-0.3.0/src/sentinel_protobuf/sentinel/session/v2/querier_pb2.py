
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....sentinel.session.v2 import params_pb2 as sentinel_dot_session_dot_v2_dot_params__pb2
from ....sentinel.session.v2 import session_pb2 as sentinel_dot_session_dot_v2_dot_session__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!sentinel/session/v2/querier.proto\x12\x13sentinel.session.v2\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a sentinel/session/v2/params.proto\x1a!sentinel/session/v2/session.proto"R\n\x14QuerySessionsRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"m\n\x1eQuerySessionsForAccountRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"j\n\x1bQuerySessionsForNodeRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"m\n#QuerySessionsForSubscriptionRequest\x12\n\n\x02id\x18\x01 \x01(\x04\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"|\n!QuerySessionsForAllocationRequest\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0f\n\x07address\x18\x02 \x01(\t\x12:\n\npagination\x18\x03 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"!\n\x13QuerySessionRequest\x12\n\n\x02id\x18\x01 \x01(\x04"\x14\n\x12QueryParamsRequest"\x8a\x01\n\x15QuerySessionsResponse\x124\n\x08sessions\x18\x01 \x03(\x0b2\x1c.sentinel.session.v2.SessionB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x94\x01\n\x1fQuerySessionsForAccountResponse\x124\n\x08sessions\x18\x01 \x03(\x0b2\x1c.sentinel.session.v2.SessionB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x91\x01\n\x1cQuerySessionsForNodeResponse\x124\n\x08sessions\x18\x01 \x03(\x0b2\x1c.sentinel.session.v2.SessionB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x99\x01\n$QuerySessionsForSubscriptionResponse\x124\n\x08sessions\x18\x01 \x03(\x0b2\x1c.sentinel.session.v2.SessionB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x97\x01\n"QuerySessionsForAllocationResponse\x124\n\x08sessions\x18\x01 \x03(\x0b2\x1c.sentinel.session.v2.SessionB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"K\n\x14QuerySessionResponse\x123\n\x07session\x18\x01 \x01(\x0b2\x1c.sentinel.session.v2.SessionB\x04\xc8\xde\x1f\x00"H\n\x13QueryParamsResponse\x121\n\x06params\x18\x01 \x01(\x0b2\x1b.sentinel.session.v2.ParamsB\x04\xc8\xde\x1f\x002\xa1\t\n\x0cQueryService\x12\x82\x01\n\rQuerySessions\x12).sentinel.session.v2.QuerySessionsRequest\x1a*.sentinel.session.v2.QuerySessionsResponse"\x1a\x82\xd3\xe4\x93\x02\x14\x12\x12/sentinel/sessions\x12\xb3\x01\n\x17QuerySessionsForAccount\x123.sentinel.session.v2.QuerySessionsForAccountRequest\x1a4.sentinel.session.v2.QuerySessionsForAccountResponse"-\x82\xd3\xe4\x93\x02\'\x12%/sentinel/accounts/{address}/sessions\x12\xa7\x01\n\x14QuerySessionsForNode\x120.sentinel.session.v2.QuerySessionsForNodeRequest\x1a1.sentinel.session.v2.QuerySessionsForNodeResponse"*\x82\xd3\xe4\x93\x02$\x12"/sentinel/nodes/{address}/sessions\x12\xc2\x01\n\x1cQuerySessionsForSubscription\x128.sentinel.session.v2.QuerySessionsForSubscriptionRequest\x1a9.sentinel.session.v2.QuerySessionsForSubscriptionResponse"-\x82\xd3\xe4\x93\x02\'\x12%/sentinel/subscriptions/{id}/sessions\x12\xd2\x01\n\x1aQuerySessionsForAllocation\x126.sentinel.session.v2.QuerySessionsForAllocationRequest\x1a7.sentinel.session.v2.QuerySessionsForAllocationResponse"C\x82\xd3\xe4\x93\x02=\x12;/sentinel/subscriptions/{id}/allocations/{address}/sessions\x12\x84\x01\n\x0cQuerySession\x12(.sentinel.session.v2.QuerySessionRequest\x1a).sentinel.session.v2.QuerySessionResponse"\x1f\x82\xd3\xe4\x93\x02\x19\x12\x17/sentinel/sessions/{id}\x12\x8a\x01\n\x0bQueryParams\x12\'.sentinel.session.v2.QueryParamsRequest\x1a(.sentinel.session.v2.QueryParamsResponse"(\x82\xd3\xe4\x93\x02"\x12 /sentinel/modules/session/paramsB:Z0github.com/sentinel-official/hub/x/session/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.session.v2.querier_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/sentinel-official/hub/x/session/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _QUERYSESSIONSRESPONSE.fields_by_name['sessions']._options = None
    _QUERYSESSIONSRESPONSE.fields_by_name['sessions']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSESSIONSFORACCOUNTRESPONSE.fields_by_name['sessions']._options = None
    _QUERYSESSIONSFORACCOUNTRESPONSE.fields_by_name['sessions']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSESSIONSFORNODERESPONSE.fields_by_name['sessions']._options = None
    _QUERYSESSIONSFORNODERESPONSE.fields_by_name['sessions']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSESSIONSFORSUBSCRIPTIONRESPONSE.fields_by_name['sessions']._options = None
    _QUERYSESSIONSFORSUBSCRIPTIONRESPONSE.fields_by_name['sessions']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSESSIONSFORALLOCATIONRESPONSE.fields_by_name['sessions']._options = None
    _QUERYSESSIONSFORALLOCATIONRESPONSE.fields_by_name['sessions']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSESSIONRESPONSE.fields_by_name['session']._options = None
    _QUERYSESSIONRESPONSE.fields_by_name['session']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSERVICE.methods_by_name['QuerySessions']._options = None
    _QUERYSERVICE.methods_by_name['QuerySessions']._serialized_options = b'\x82\xd3\xe4\x93\x02\x14\x12\x12/sentinel/sessions'
    _QUERYSERVICE.methods_by_name['QuerySessionsForAccount']._options = None
    _QUERYSERVICE.methods_by_name['QuerySessionsForAccount']._serialized_options = b"\x82\xd3\xe4\x93\x02'\x12%/sentinel/accounts/{address}/sessions"
    _QUERYSERVICE.methods_by_name['QuerySessionsForNode']._options = None
    _QUERYSERVICE.methods_by_name['QuerySessionsForNode']._serialized_options = b'\x82\xd3\xe4\x93\x02$\x12"/sentinel/nodes/{address}/sessions'
    _QUERYSERVICE.methods_by_name['QuerySessionsForSubscription']._options = None
    _QUERYSERVICE.methods_by_name['QuerySessionsForSubscription']._serialized_options = b"\x82\xd3\xe4\x93\x02'\x12%/sentinel/subscriptions/{id}/sessions"
    _QUERYSERVICE.methods_by_name['QuerySessionsForAllocation']._options = None
    _QUERYSERVICE.methods_by_name['QuerySessionsForAllocation']._serialized_options = b'\x82\xd3\xe4\x93\x02=\x12;/sentinel/subscriptions/{id}/allocations/{address}/sessions'
    _QUERYSERVICE.methods_by_name['QuerySession']._options = None
    _QUERYSERVICE.methods_by_name['QuerySession']._serialized_options = b'\x82\xd3\xe4\x93\x02\x19\x12\x17/sentinel/sessions/{id}'
    _QUERYSERVICE.methods_by_name['QueryParams']._options = None
    _QUERYSERVICE.methods_by_name['QueryParams']._serialized_options = b'\x82\xd3\xe4\x93\x02"\x12 /sentinel/modules/session/params'
    _QUERYSESSIONSREQUEST._serialized_start = 223
    _QUERYSESSIONSREQUEST._serialized_end = 305
    _QUERYSESSIONSFORACCOUNTREQUEST._serialized_start = 307
    _QUERYSESSIONSFORACCOUNTREQUEST._serialized_end = 416
    _QUERYSESSIONSFORNODEREQUEST._serialized_start = 418
    _QUERYSESSIONSFORNODEREQUEST._serialized_end = 524
    _QUERYSESSIONSFORSUBSCRIPTIONREQUEST._serialized_start = 526
    _QUERYSESSIONSFORSUBSCRIPTIONREQUEST._serialized_end = 635
    _QUERYSESSIONSFORALLOCATIONREQUEST._serialized_start = 637
    _QUERYSESSIONSFORALLOCATIONREQUEST._serialized_end = 761
    _QUERYSESSIONREQUEST._serialized_start = 763
    _QUERYSESSIONREQUEST._serialized_end = 796
    _QUERYPARAMSREQUEST._serialized_start = 798
    _QUERYPARAMSREQUEST._serialized_end = 818
    _QUERYSESSIONSRESPONSE._serialized_start = 821
    _QUERYSESSIONSRESPONSE._serialized_end = 959
    _QUERYSESSIONSFORACCOUNTRESPONSE._serialized_start = 962
    _QUERYSESSIONSFORACCOUNTRESPONSE._serialized_end = 1110
    _QUERYSESSIONSFORNODERESPONSE._serialized_start = 1113
    _QUERYSESSIONSFORNODERESPONSE._serialized_end = 1258
    _QUERYSESSIONSFORSUBSCRIPTIONRESPONSE._serialized_start = 1261
    _QUERYSESSIONSFORSUBSCRIPTIONRESPONSE._serialized_end = 1414
    _QUERYSESSIONSFORALLOCATIONRESPONSE._serialized_start = 1417
    _QUERYSESSIONSFORALLOCATIONRESPONSE._serialized_end = 1568
    _QUERYSESSIONRESPONSE._serialized_start = 1570
    _QUERYSESSIONRESPONSE._serialized_end = 1645
    _QUERYPARAMSRESPONSE._serialized_start = 1647
    _QUERYPARAMSRESPONSE._serialized_end = 1719
    _QUERYSERVICE._serialized_start = 1722
    _QUERYSERVICE._serialized_end = 2907
