
'Client and server classes corresponding to protobuf-defined services.'
import grpc

class QueryStub(object):
    'Query defines the gRPC querier service.\n    this line is used by starport scaffolding # 2\n    '

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '

class QueryServicer(object):
    'Query defines the gRPC querier service.\n    this line is used by starport scaffolding # 2\n    '

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {}
    generic_handler = grpc.method_handlers_generic_handler('interchain_security.ccv.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class Query(object):
    'Query defines the gRPC querier service.\n    this line is used by starport scaffolding # 2\n    '
