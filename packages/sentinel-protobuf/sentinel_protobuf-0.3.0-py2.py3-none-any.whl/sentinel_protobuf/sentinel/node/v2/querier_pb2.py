
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
from ....sentinel.node.v2 import node_pb2 as sentinel_dot_node_dot_v2_dot_node__pb2
from ....sentinel.node.v2 import params_pb2 as sentinel_dot_node_dot_v2_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1esentinel/node/v2/querier.proto\x12\x10sentinel.node.v2\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1esentinel/types/v1/status.proto\x1a\x1bsentinel/node/v2/node.proto\x1a\x1dsentinel/node/v2/params.proto"z\n\x11QueryNodesRequest\x12)\n\x06status\x18\x01 \x01(\x0e2\x19.sentinel.types.v1.Status\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x8d\x01\n\x18QueryNodesForPlanRequest\x12\n\n\x02id\x18\x01 \x01(\x04\x12)\n\x06status\x18\x02 \x01(\x0e2\x19.sentinel.types.v1.Status\x12:\n\npagination\x18\x03 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"#\n\x10QueryNodeRequest\x12\x0f\n\x07address\x18\x01 \x01(\t"\x14\n\x12QueryParamsRequest"~\n\x12QueryNodesResponse\x12+\n\x05nodes\x18\x01 \x03(\x0b2\x16.sentinel.node.v2.NodeB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x85\x01\n\x19QueryNodesForPlanResponse\x12+\n\x05nodes\x18\x01 \x03(\x0b2\x16.sentinel.node.v2.NodeB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"?\n\x11QueryNodeResponse\x12*\n\x04node\x18\x01 \x01(\x0b2\x16.sentinel.node.v2.NodeB\x04\xc8\xde\x1f\x00"E\n\x13QueryParamsResponse\x12.\n\x06params\x18\x01 \x01(\x0b2\x18.sentinel.node.v2.ParamsB\x04\xc8\xde\x1f\x002\x90\x04\n\x0cQueryService\x12p\n\nQueryNodes\x12#.sentinel.node.v2.QueryNodesRequest\x1a$.sentinel.node.v2.QueryNodesResponse"\x17\x82\xd3\xe4\x93\x02\x11\x12\x0f/sentinel/nodes\x12\x90\x01\n\x11QueryNodesForPlan\x12*.sentinel.node.v2.QueryNodesForPlanRequest\x1a+.sentinel.node.v2.QueryNodesForPlanResponse""\x82\xd3\xe4\x93\x02\x1c\x12\x1a/sentinel/plans/{id}/nodes\x12w\n\tQueryNode\x12".sentinel.node.v2.QueryNodeRequest\x1a#.sentinel.node.v2.QueryNodeResponse"!\x82\xd3\xe4\x93\x02\x1b\x12\x19/sentinel/nodes/{address}\x12\x81\x01\n\x0bQueryParams\x12$.sentinel.node.v2.QueryParamsRequest\x1a%.sentinel.node.v2.QueryParamsResponse"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/sentinel/modules/node/paramsB7Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.node.v2.querier_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _QUERYNODESRESPONSE.fields_by_name['nodes']._options = None
    _QUERYNODESRESPONSE.fields_by_name['nodes']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYNODESFORPLANRESPONSE.fields_by_name['nodes']._options = None
    _QUERYNODESFORPLANRESPONSE.fields_by_name['nodes']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYNODERESPONSE.fields_by_name['node']._options = None
    _QUERYNODERESPONSE.fields_by_name['node']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSERVICE.methods_by_name['QueryNodes']._options = None
    _QUERYSERVICE.methods_by_name['QueryNodes']._serialized_options = b'\x82\xd3\xe4\x93\x02\x11\x12\x0f/sentinel/nodes'
    _QUERYSERVICE.methods_by_name['QueryNodesForPlan']._options = None
    _QUERYSERVICE.methods_by_name['QueryNodesForPlan']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1c\x12\x1a/sentinel/plans/{id}/nodes'
    _QUERYSERVICE.methods_by_name['QueryNode']._options = None
    _QUERYSERVICE.methods_by_name['QueryNode']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1b\x12\x19/sentinel/nodes/{address}'
    _QUERYSERVICE.methods_by_name['QueryParams']._options = None
    _QUERYSERVICE.methods_by_name['QueryParams']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1f\x12\x1d/sentinel/modules/node/params'
    _QUERYNODESREQUEST._serialized_start = 240
    _QUERYNODESREQUEST._serialized_end = 362
    _QUERYNODESFORPLANREQUEST._serialized_start = 365
    _QUERYNODESFORPLANREQUEST._serialized_end = 506
    _QUERYNODEREQUEST._serialized_start = 508
    _QUERYNODEREQUEST._serialized_end = 543
    _QUERYPARAMSREQUEST._serialized_start = 545
    _QUERYPARAMSREQUEST._serialized_end = 565
    _QUERYNODESRESPONSE._serialized_start = 567
    _QUERYNODESRESPONSE._serialized_end = 693
    _QUERYNODESFORPLANRESPONSE._serialized_start = 696
    _QUERYNODESFORPLANRESPONSE._serialized_end = 829
    _QUERYNODERESPONSE._serialized_start = 831
    _QUERYNODERESPONSE._serialized_end = 894
    _QUERYPARAMSRESPONSE._serialized_start = 896
    _QUERYPARAMSRESPONSE._serialized_end = 965
    _QUERYSERVICE._serialized_start = 968
    _QUERYSERVICE._serialized_end = 1496
