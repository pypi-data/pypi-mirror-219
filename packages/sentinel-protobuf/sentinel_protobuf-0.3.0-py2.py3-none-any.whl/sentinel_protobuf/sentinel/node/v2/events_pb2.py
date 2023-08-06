
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsentinel/node/v2/events.proto\x12\x10sentinel.node.v2\x1a\x14gogoproto/gogo.proto\x1a\x1esentinel/types/v1/status.proto"4\n\rEventRegister\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address""9\n\x12EventUpdateDetails\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address""v\n\x11EventUpdateStatus\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12<\n\x06status\x18\x02 \x01(\x0e2\x19.sentinel.types.v1.StatusB\x11\xf2\xde\x1f\ryaml:"status""i\n\x17EventCreateSubscription\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12-\n\x0cnode_address\x18\x02 \x01(\tB\x17\xf2\xde\x1f\x13yaml:"node_address"B7Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.node.v2.events_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/node/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _EVENTREGISTER.fields_by_name['address']._options = None
    _EVENTREGISTER.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTUPDATEDETAILS.fields_by_name['address']._options = None
    _EVENTUPDATEDETAILS.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTUPDATESTATUS.fields_by_name['address']._options = None
    _EVENTUPDATESTATUS.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTUPDATESTATUS.fields_by_name['status']._options = None
    _EVENTUPDATESTATUS.fields_by_name['status']._serialized_options = b'\xf2\xde\x1f\ryaml:"status"'
    _EVENTCREATESUBSCRIPTION.fields_by_name['id']._options = None
    _EVENTCREATESUBSCRIPTION.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTCREATESUBSCRIPTION.fields_by_name['node_address']._options = None
    _EVENTCREATESUBSCRIPTION.fields_by_name['node_address']._serialized_options = b'\xf2\xde\x1f\x13yaml:"node_address"'
    _EVENTREGISTER._serialized_start = 105
    _EVENTREGISTER._serialized_end = 157
    _EVENTUPDATEDETAILS._serialized_start = 159
    _EVENTUPDATEDETAILS._serialized_end = 216
    _EVENTUPDATESTATUS._serialized_start = 218
    _EVENTUPDATESTATUS._serialized_end = 336
    _EVENTCREATESUBSCRIPTION._serialized_start = 338
    _EVENTCREATESUBSCRIPTION._serialized_end = 443
