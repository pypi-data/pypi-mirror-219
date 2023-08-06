
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n sentinel/session/v2/events.proto\x12\x13sentinel.session.v2\x1a\x14gogoproto/gogo.proto\x1a\x1esentinel/types/v1/status.proto"\xa3\x01\n\nEventStart\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12E\n\x0fsubscription_id\x18\x02 \x01(\x04B,\xe2\xde\x1f\x0eSubscriptionID\xf2\xde\x1f\x16yaml:"subscription_id"\x12-\n\x0cnode_address\x18\x03 \x01(\tB\x17\xf2\xde\x1f\x13yaml:"node_address""\xab\x01\n\x12EventUpdateDetails\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12E\n\x0fsubscription_id\x18\x02 \x01(\x04B,\xe2\xde\x1f\x0eSubscriptionID\xf2\xde\x1f\x16yaml:"subscription_id"\x12-\n\x0cnode_address\x18\x03 \x01(\tB\x17\xf2\xde\x1f\x13yaml:"node_address""\xe8\x01\n\x11EventUpdateStatus\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12E\n\x0fsubscription_id\x18\x02 \x01(\x04B,\xe2\xde\x1f\x0eSubscriptionID\xf2\xde\x1f\x16yaml:"subscription_id"\x12-\n\x0cnode_address\x18\x03 \x01(\tB\x17\xf2\xde\x1f\x13yaml:"node_address"\x12<\n\x06status\x18\x04 \x01(\x0e2\x19.sentinel.types.v1.StatusB\x11\xf2\xde\x1f\ryaml:"status"B:Z0github.com/sentinel-official/hub/x/session/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.session.v2.events_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/sentinel-official/hub/x/session/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _EVENTSTART.fields_by_name['id']._options = None
    _EVENTSTART.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTSTART.fields_by_name['subscription_id']._options = None
    _EVENTSTART.fields_by_name['subscription_id']._serialized_options = b'\xe2\xde\x1f\x0eSubscriptionID\xf2\xde\x1f\x16yaml:"subscription_id"'
    _EVENTSTART.fields_by_name['node_address']._options = None
    _EVENTSTART.fields_by_name['node_address']._serialized_options = b'\xf2\xde\x1f\x13yaml:"node_address"'
    _EVENTUPDATEDETAILS.fields_by_name['id']._options = None
    _EVENTUPDATEDETAILS.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTUPDATEDETAILS.fields_by_name['subscription_id']._options = None
    _EVENTUPDATEDETAILS.fields_by_name['subscription_id']._serialized_options = b'\xe2\xde\x1f\x0eSubscriptionID\xf2\xde\x1f\x16yaml:"subscription_id"'
    _EVENTUPDATEDETAILS.fields_by_name['node_address']._options = None
    _EVENTUPDATEDETAILS.fields_by_name['node_address']._serialized_options = b'\xf2\xde\x1f\x13yaml:"node_address"'
    _EVENTUPDATESTATUS.fields_by_name['id']._options = None
    _EVENTUPDATESTATUS.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTUPDATESTATUS.fields_by_name['subscription_id']._options = None
    _EVENTUPDATESTATUS.fields_by_name['subscription_id']._serialized_options = b'\xe2\xde\x1f\x0eSubscriptionID\xf2\xde\x1f\x16yaml:"subscription_id"'
    _EVENTUPDATESTATUS.fields_by_name['node_address']._options = None
    _EVENTUPDATESTATUS.fields_by_name['node_address']._serialized_options = b'\xf2\xde\x1f\x13yaml:"node_address"'
    _EVENTUPDATESTATUS.fields_by_name['status']._options = None
    _EVENTUPDATESTATUS.fields_by_name['status']._serialized_options = b'\xf2\xde\x1f\ryaml:"status"'
    _EVENTSTART._serialized_start = 112
    _EVENTSTART._serialized_end = 275
    _EVENTUPDATEDETAILS._serialized_start = 278
    _EVENTUPDATEDETAILS._serialized_end = 449
    _EVENTUPDATESTATUS._serialized_start = 452
    _EVENTUPDATESTATUS._serialized_end = 684
