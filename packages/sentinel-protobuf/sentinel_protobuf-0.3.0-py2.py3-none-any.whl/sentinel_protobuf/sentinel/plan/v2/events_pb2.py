
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsentinel/plan/v2/events.proto\x12\x10sentinel.plan.v2\x1a\x14gogoproto/gogo.proto\x1a\x1esentinel/types/v1/status.proto".\n\x0bEventCreate\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id""r\n\x11EventUpdateStatus\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12<\n\x06status\x18\x03 \x01(\x0e2\x19.sentinel.types.v1.StatusB\x11\xf2\xde\x1f\ryaml:"status""U\n\rEventLinkNode\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12#\n\x07address\x18\x02 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address""W\n\x0fEventUnlinkNode\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12#\n\x07address\x18\x02 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address""i\n\x17EventCreateSubscription\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12-\n\x07plan_id\x18\x02 \x01(\x04B\x1c\xe2\xde\x1f\x06PlanID\xf2\xde\x1f\x0eyaml:"plan_id"B7Z-github.com/sentinel-official/hub/x/plan/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.plan.v2.events_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/plan/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _EVENTCREATE.fields_by_name['id']._options = None
    _EVENTCREATE.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTUPDATESTATUS.fields_by_name['id']._options = None
    _EVENTUPDATESTATUS.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTUPDATESTATUS.fields_by_name['status']._options = None
    _EVENTUPDATESTATUS.fields_by_name['status']._serialized_options = b'\xf2\xde\x1f\ryaml:"status"'
    _EVENTLINKNODE.fields_by_name['id']._options = None
    _EVENTLINKNODE.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTLINKNODE.fields_by_name['address']._options = None
    _EVENTLINKNODE.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTUNLINKNODE.fields_by_name['id']._options = None
    _EVENTUNLINKNODE.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTUNLINKNODE.fields_by_name['address']._options = None
    _EVENTUNLINKNODE.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTCREATESUBSCRIPTION.fields_by_name['id']._options = None
    _EVENTCREATESUBSCRIPTION.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTCREATESUBSCRIPTION.fields_by_name['plan_id']._options = None
    _EVENTCREATESUBSCRIPTION.fields_by_name['plan_id']._serialized_options = b'\xe2\xde\x1f\x06PlanID\xf2\xde\x1f\x0eyaml:"plan_id"'
    _EVENTCREATE._serialized_start = 105
    _EVENTCREATE._serialized_end = 151
    _EVENTUPDATESTATUS._serialized_start = 153
    _EVENTUPDATESTATUS._serialized_end = 267
    _EVENTLINKNODE._serialized_start = 269
    _EVENTLINKNODE._serialized_end = 354
    _EVENTUNLINKNODE._serialized_start = 356
    _EVENTUNLINKNODE._serialized_end = 443
    _EVENTCREATESUBSCRIPTION._serialized_start = 445
    _EVENTCREATESUBSCRIPTION._serialized_end = 550
