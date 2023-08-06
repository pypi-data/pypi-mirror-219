
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....sentinel.subscription.v2 import allocation_pb2 as sentinel_dot_subscription_dot_v2_dot_allocation__pb2
from ....sentinel.subscription.v2 import params_pb2 as sentinel_dot_subscription_dot_v2_dot_params__pb2
from ....sentinel.subscription.v2 import payout_pb2 as sentinel_dot_subscription_dot_v2_dot_payout__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&sentinel/subscription/v2/querier.proto\x12\x18sentinel.subscription.v2\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x19google/protobuf/any.proto\x1a)sentinel/subscription/v2/allocation.proto\x1a%sentinel/subscription/v2/params.proto\x1a%sentinel/subscription/v2/payout.proto"W\n\x19QuerySubscriptionsRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"r\n#QuerySubscriptionsForAccountRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"o\n QuerySubscriptionsForNodeRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"j\n QuerySubscriptionsForPlanRequest\x12\n\n\x02id\x18\x01 \x01(\x04\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"&\n\x18QuerySubscriptionRequest\x12\n\n\x02id\x18\x01 \x01(\x04"5\n\x16QueryAllocationRequest\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0f\n\x07address\x18\x02 \x01(\t"a\n\x17QueryAllocationsRequest\x12\n\n\x02id\x18\x01 \x01(\x04\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"Q\n\x13QueryPayoutsRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"l\n\x1dQueryPayoutsForAccountRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"i\n\x1aQueryPayoutsForNodeRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest" \n\x12QueryPayoutRequest\x12\n\n\x02id\x18\x01 \x01(\x04"\x14\n\x12QueryParamsRequest"\x86\x01\n\x1aQuerySubscriptionsResponse\x12+\n\rsubscriptions\x18\x01 \x03(\x0b2\x14.google.protobuf.Any\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x90\x01\n$QuerySubscriptionsForAccountResponse\x12+\n\rsubscriptions\x18\x01 \x03(\x0b2\x14.google.protobuf.Any\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x8d\x01\n!QuerySubscriptionsForNodeResponse\x12+\n\rsubscriptions\x18\x01 \x03(\x0b2\x14.google.protobuf.Any\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x8d\x01\n!QuerySubscriptionsForPlanResponse\x12+\n\rsubscriptions\x18\x01 \x03(\x0b2\x14.google.protobuf.Any\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"G\n\x19QuerySubscriptionResponse\x12*\n\x0csubscription\x18\x01 \x01(\x0b2\x14.google.protobuf.Any"Y\n\x17QueryAllocationResponse\x12>\n\nallocation\x18\x01 \x01(\x0b2$.sentinel.subscription.v2.AllocationB\x04\xc8\xde\x1f\x00"\x98\x01\n\x18QueryAllocationsResponse\x12?\n\x0ballocations\x18\x01 \x03(\x0b2$.sentinel.subscription.v2.AllocationB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x8c\x01\n\x14QueryPayoutsResponse\x127\n\x07payouts\x18\x01 \x03(\x0b2 .sentinel.subscription.v2.PayoutB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x96\x01\n\x1eQueryPayoutsForAccountResponse\x127\n\x07payouts\x18\x01 \x03(\x0b2 .sentinel.subscription.v2.PayoutB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x93\x01\n\x1bQueryPayoutsForNodeResponse\x127\n\x07payouts\x18\x01 \x03(\x0b2 .sentinel.subscription.v2.PayoutB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"M\n\x13QueryPayoutResponse\x126\n\x06payout\x18\x01 \x01(\x0b2 .sentinel.subscription.v2.PayoutB\x04\xc8\xde\x1f\x00"M\n\x13QueryParamsResponse\x126\n\x06params\x18\x01 \x01(\x0b2 .sentinel.subscription.v2.ParamsB\x04\xc8\xde\x1f\x002\xb8\x10\n\x0cQueryService\x12\xa0\x01\n\x12QuerySubscriptions\x123.sentinel.subscription.v2.QuerySubscriptionsRequest\x1a4.sentinel.subscription.v2.QuerySubscriptionsResponse"\x1f\x82\xd3\xe4\x93\x02\x19\x12\x17/sentinel/subscriptions\x12\xd1\x01\n\x1cQuerySubscriptionsForAccount\x12=.sentinel.subscription.v2.QuerySubscriptionsForAccountRequest\x1a>.sentinel.subscription.v2.QuerySubscriptionsForAccountResponse"2\x82\xd3\xe4\x93\x02,\x12*/sentinel/accounts/{address}/subscriptions\x12\xc5\x01\n\x19QuerySubscriptionsForNode\x12:.sentinel.subscription.v2.QuerySubscriptionsForNodeRequest\x1a;.sentinel.subscription.v2.QuerySubscriptionsForNodeResponse"/\x82\xd3\xe4\x93\x02)\x12\'/sentinel/nodes/{address}/subscriptions\x12\xc0\x01\n\x19QuerySubscriptionsForPlan\x12:.sentinel.subscription.v2.QuerySubscriptionsForPlanRequest\x1a;.sentinel.subscription.v2.QuerySubscriptionsForPlanResponse"*\x82\xd3\xe4\x93\x02$\x12"/sentinel/plans/{id}/subscriptions\x12\xa2\x01\n\x11QuerySubscription\x122.sentinel.subscription.v2.QuerySubscriptionRequest\x1a3.sentinel.subscription.v2.QuerySubscriptionResponse"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/sentinel/subscriptions/{id}\x12\xab\x01\n\x10QueryAllocations\x121.sentinel.subscription.v2.QueryAllocationsRequest\x1a2.sentinel.subscription.v2.QueryAllocationsResponse"0\x82\xd3\xe4\x93\x02*\x12(/sentinel/subscriptions/{id}/allocations\x12\xb2\x01\n\x0fQueryAllocation\x120.sentinel.subscription.v2.QueryAllocationRequest\x1a1.sentinel.subscription.v2.QueryAllocationResponse":\x82\xd3\xe4\x93\x024\x122/sentinel/subscriptions/{id}/allocations/{address}\x12\x88\x01\n\x0cQueryPayouts\x12-.sentinel.subscription.v2.QueryPayoutsRequest\x1a..sentinel.subscription.v2.QueryPayoutsResponse"\x19\x82\xd3\xe4\x93\x02\x13\x12\x11/sentinel/payouts\x12\xb9\x01\n\x16QueryPayoutsForAccount\x127.sentinel.subscription.v2.QueryPayoutsForAccountRequest\x1a8.sentinel.subscription.v2.QueryPayoutsForAccountResponse",\x82\xd3\xe4\x93\x02&\x12$/sentinel/accounts/{address}/payouts\x12\xad\x01\n\x13QueryPayoutsForNode\x124.sentinel.subscription.v2.QueryPayoutsForNodeRequest\x1a5.sentinel.subscription.v2.QueryPayoutsForNodeResponse")\x82\xd3\xe4\x93\x02#\x12!/sentinel/nodes/{address}/payouts\x12\x8a\x01\n\x0bQueryPayout\x12,.sentinel.subscription.v2.QueryPayoutRequest\x1a-.sentinel.subscription.v2.QueryPayoutResponse"\x1e\x82\xd3\xe4\x93\x02\x18\x12\x16/sentinel/payouts/{id}\x12\x99\x01\n\x0bQueryParams\x12,.sentinel.subscription.v2.QueryParamsRequest\x1a-.sentinel.subscription.v2.QueryParamsResponse"-\x82\xd3\xe4\x93\x02\'\x12%/sentinel/modules/subscription/paramsB?Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.subscription.v2.querier_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _QUERYALLOCATIONRESPONSE.fields_by_name['allocation']._options = None
    _QUERYALLOCATIONRESPONSE.fields_by_name['allocation']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYALLOCATIONSRESPONSE.fields_by_name['allocations']._options = None
    _QUERYALLOCATIONSRESPONSE.fields_by_name['allocations']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPAYOUTSRESPONSE.fields_by_name['payouts']._options = None
    _QUERYPAYOUTSRESPONSE.fields_by_name['payouts']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPAYOUTSFORACCOUNTRESPONSE.fields_by_name['payouts']._options = None
    _QUERYPAYOUTSFORACCOUNTRESPONSE.fields_by_name['payouts']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPAYOUTSFORNODERESPONSE.fields_by_name['payouts']._options = None
    _QUERYPAYOUTSFORNODERESPONSE.fields_by_name['payouts']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPAYOUTRESPONSE.fields_by_name['payout']._options = None
    _QUERYPAYOUTRESPONSE.fields_by_name['payout']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSERVICE.methods_by_name['QuerySubscriptions']._options = None
    _QUERYSERVICE.methods_by_name['QuerySubscriptions']._serialized_options = b'\x82\xd3\xe4\x93\x02\x19\x12\x17/sentinel/subscriptions'
    _QUERYSERVICE.methods_by_name['QuerySubscriptionsForAccount']._options = None
    _QUERYSERVICE.methods_by_name['QuerySubscriptionsForAccount']._serialized_options = b'\x82\xd3\xe4\x93\x02,\x12*/sentinel/accounts/{address}/subscriptions'
    _QUERYSERVICE.methods_by_name['QuerySubscriptionsForNode']._options = None
    _QUERYSERVICE.methods_by_name['QuerySubscriptionsForNode']._serialized_options = b"\x82\xd3\xe4\x93\x02)\x12'/sentinel/nodes/{address}/subscriptions"
    _QUERYSERVICE.methods_by_name['QuerySubscriptionsForPlan']._options = None
    _QUERYSERVICE.methods_by_name['QuerySubscriptionsForPlan']._serialized_options = b'\x82\xd3\xe4\x93\x02$\x12"/sentinel/plans/{id}/subscriptions'
    _QUERYSERVICE.methods_by_name['QuerySubscription']._options = None
    _QUERYSERVICE.methods_by_name['QuerySubscription']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1e\x12\x1c/sentinel/subscriptions/{id}'
    _QUERYSERVICE.methods_by_name['QueryAllocations']._options = None
    _QUERYSERVICE.methods_by_name['QueryAllocations']._serialized_options = b'\x82\xd3\xe4\x93\x02*\x12(/sentinel/subscriptions/{id}/allocations'
    _QUERYSERVICE.methods_by_name['QueryAllocation']._options = None
    _QUERYSERVICE.methods_by_name['QueryAllocation']._serialized_options = b'\x82\xd3\xe4\x93\x024\x122/sentinel/subscriptions/{id}/allocations/{address}'
    _QUERYSERVICE.methods_by_name['QueryPayouts']._options = None
    _QUERYSERVICE.methods_by_name['QueryPayouts']._serialized_options = b'\x82\xd3\xe4\x93\x02\x13\x12\x11/sentinel/payouts'
    _QUERYSERVICE.methods_by_name['QueryPayoutsForAccount']._options = None
    _QUERYSERVICE.methods_by_name['QueryPayoutsForAccount']._serialized_options = b'\x82\xd3\xe4\x93\x02&\x12$/sentinel/accounts/{address}/payouts'
    _QUERYSERVICE.methods_by_name['QueryPayoutsForNode']._options = None
    _QUERYSERVICE.methods_by_name['QueryPayoutsForNode']._serialized_options = b'\x82\xd3\xe4\x93\x02#\x12!/sentinel/nodes/{address}/payouts'
    _QUERYSERVICE.methods_by_name['QueryPayout']._options = None
    _QUERYSERVICE.methods_by_name['QueryPayout']._serialized_options = b'\x82\xd3\xe4\x93\x02\x18\x12\x16/sentinel/payouts/{id}'
    _QUERYSERVICE.methods_by_name['QueryParams']._options = None
    _QUERYSERVICE.methods_by_name['QueryParams']._serialized_options = b"\x82\xd3\xe4\x93\x02'\x12%/sentinel/modules/subscription/params"
    _QUERYSUBSCRIPTIONSREQUEST._serialized_start = 312
    _QUERYSUBSCRIPTIONSREQUEST._serialized_end = 399
    _QUERYSUBSCRIPTIONSFORACCOUNTREQUEST._serialized_start = 401
    _QUERYSUBSCRIPTIONSFORACCOUNTREQUEST._serialized_end = 515
    _QUERYSUBSCRIPTIONSFORNODEREQUEST._serialized_start = 517
    _QUERYSUBSCRIPTIONSFORNODEREQUEST._serialized_end = 628
    _QUERYSUBSCRIPTIONSFORPLANREQUEST._serialized_start = 630
    _QUERYSUBSCRIPTIONSFORPLANREQUEST._serialized_end = 736
    _QUERYSUBSCRIPTIONREQUEST._serialized_start = 738
    _QUERYSUBSCRIPTIONREQUEST._serialized_end = 776
    _QUERYALLOCATIONREQUEST._serialized_start = 778
    _QUERYALLOCATIONREQUEST._serialized_end = 831
    _QUERYALLOCATIONSREQUEST._serialized_start = 833
    _QUERYALLOCATIONSREQUEST._serialized_end = 930
    _QUERYPAYOUTSREQUEST._serialized_start = 932
    _QUERYPAYOUTSREQUEST._serialized_end = 1013
    _QUERYPAYOUTSFORACCOUNTREQUEST._serialized_start = 1015
    _QUERYPAYOUTSFORACCOUNTREQUEST._serialized_end = 1123
    _QUERYPAYOUTSFORNODEREQUEST._serialized_start = 1125
    _QUERYPAYOUTSFORNODEREQUEST._serialized_end = 1230
    _QUERYPAYOUTREQUEST._serialized_start = 1232
    _QUERYPAYOUTREQUEST._serialized_end = 1264
    _QUERYPARAMSREQUEST._serialized_start = 1266
    _QUERYPARAMSREQUEST._serialized_end = 1286
    _QUERYSUBSCRIPTIONSRESPONSE._serialized_start = 1289
    _QUERYSUBSCRIPTIONSRESPONSE._serialized_end = 1423
    _QUERYSUBSCRIPTIONSFORACCOUNTRESPONSE._serialized_start = 1426
    _QUERYSUBSCRIPTIONSFORACCOUNTRESPONSE._serialized_end = 1570
    _QUERYSUBSCRIPTIONSFORNODERESPONSE._serialized_start = 1573
    _QUERYSUBSCRIPTIONSFORNODERESPONSE._serialized_end = 1714
    _QUERYSUBSCRIPTIONSFORPLANRESPONSE._serialized_start = 1717
    _QUERYSUBSCRIPTIONSFORPLANRESPONSE._serialized_end = 1858
    _QUERYSUBSCRIPTIONRESPONSE._serialized_start = 1860
    _QUERYSUBSCRIPTIONRESPONSE._serialized_end = 1931
    _QUERYALLOCATIONRESPONSE._serialized_start = 1933
    _QUERYALLOCATIONRESPONSE._serialized_end = 2022
    _QUERYALLOCATIONSRESPONSE._serialized_start = 2025
    _QUERYALLOCATIONSRESPONSE._serialized_end = 2177
    _QUERYPAYOUTSRESPONSE._serialized_start = 2180
    _QUERYPAYOUTSRESPONSE._serialized_end = 2320
    _QUERYPAYOUTSFORACCOUNTRESPONSE._serialized_start = 2323
    _QUERYPAYOUTSFORACCOUNTRESPONSE._serialized_end = 2473
    _QUERYPAYOUTSFORNODERESPONSE._serialized_start = 2476
    _QUERYPAYOUTSFORNODERESPONSE._serialized_end = 2623
    _QUERYPAYOUTRESPONSE._serialized_start = 2625
    _QUERYPAYOUTRESPONSE._serialized_end = 2702
    _QUERYPARAMSRESPONSE._serialized_start = 2704
    _QUERYPARAMSRESPONSE._serialized_end = 2781
    _QUERYSERVICE._serialized_start = 2784
    _QUERYSERVICE._serialized_end = 4888
