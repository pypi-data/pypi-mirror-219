
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%sentinel/subscription/v2/events.proto\x12\x18sentinel.subscription.v2\x1a\x14gogoproto/gogo.proto\x1a\x1esentinel/types/v1/status.proto"r\n\x11EventUpdateStatus\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12<\n\x06status\x18\x02 \x01(\x0e2\x19.sentinel.types.v1.StatusB\x11\xf2\xde\x1f\ryaml:"status""\x94\x01\n\rEventAllocate\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12#\n\x07address\x18\x02 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12=\n\x05bytes\x18\x03 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00"\x82\x01\n\x0bEventPayout\x12\x1f\n\x02id\x18\x01 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12#\n\x07address\x18\x02 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12-\n\x0cnode_address\x18\x03 \x01(\tB\x17\xf2\xde\x1f\x13yaml:"node_address"B?Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.subscription.v2.events_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _EVENTUPDATESTATUS.fields_by_name['id']._options = None
    _EVENTUPDATESTATUS.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTUPDATESTATUS.fields_by_name['status']._options = None
    _EVENTUPDATESTATUS.fields_by_name['status']._serialized_options = b'\xf2\xde\x1f\ryaml:"status"'
    _EVENTALLOCATE.fields_by_name['id']._options = None
    _EVENTALLOCATE.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTALLOCATE.fields_by_name['address']._options = None
    _EVENTALLOCATE.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTALLOCATE.fields_by_name['bytes']._options = None
    _EVENTALLOCATE.fields_by_name['bytes']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00'
    _EVENTPAYOUT.fields_by_name['id']._options = None
    _EVENTPAYOUT.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTPAYOUT.fields_by_name['address']._options = None
    _EVENTPAYOUT.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTPAYOUT.fields_by_name['node_address']._options = None
    _EVENTPAYOUT.fields_by_name['node_address']._serialized_options = b'\xf2\xde\x1f\x13yaml:"node_address"'
    _EVENTUPDATESTATUS._serialized_start = 121
    _EVENTUPDATESTATUS._serialized_end = 235
    _EVENTALLOCATE._serialized_start = 238
    _EVENTALLOCATE._serialized_end = 386
    _EVENTPAYOUT._serialized_start = 389
    _EVENTPAYOUT._serialized_end = 519
