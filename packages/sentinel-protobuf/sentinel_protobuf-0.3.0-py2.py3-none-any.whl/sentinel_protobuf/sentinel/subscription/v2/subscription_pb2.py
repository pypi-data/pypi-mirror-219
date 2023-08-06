
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+sentinel/subscription/v2/subscription.proto\x12\x18sentinel.subscription.v2\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1esentinel/types/v1/status.proto"\xd4\x01\n\x10BaseSubscription\x12\x12\n\x02id\x18\x01 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x12\x0f\n\x07address\x18\x02 \x01(\t\x127\n\texpiry_at\x18\x03 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12)\n\x06status\x18\x04 \x01(\x0e2\x19.sentinel.types.v1.Status\x127\n\tstatus_at\x18\x05 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01"\xbc\x01\n\x10NodeSubscription\x12>\n\x04base\x18\x01 \x01(\x0b2*.sentinel.subscription.v2.BaseSubscriptionB\x04\xd0\xde\x1f\x01\x12\x14\n\x0cnode_address\x18\x02 \x01(\t\x12\x11\n\tgigabytes\x18\x03 \x01(\x03\x12\r\n\x05hours\x18\x04 \x01(\x03\x120\n\x07deposit\x18\x05 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00"~\n\x10PlanSubscription\x12>\n\x04base\x18\x01 \x01(\x0b2*.sentinel.subscription.v2.BaseSubscriptionB\x04\xd0\xde\x1f\x01\x12\x1b\n\x07plan_id\x18\x02 \x01(\x04B\n\xe2\xde\x1f\x06PlanID\x12\r\n\x05denom\x18\x03 \x01(\t*}\n\x10SubscriptionType\x12)\n\x10TYPE_UNSPECIFIED\x10\x00\x1a\x13\x8a\x9d \x0fTypeUnspecified\x12\x1b\n\tTYPE_NODE\x10\x01\x1a\x0c\x8a\x9d \x08TypeNode\x12\x1b\n\tTYPE_PLAN\x10\x02\x1a\x0c\x8a\x9d \x08TypePlan\x1a\x04\x88\xa3\x1e\x00B?Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.subscription.v2.subscription_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z5github.com/sentinel-official/hub/x/subscription/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _SUBSCRIPTIONTYPE._options = None
    _SUBSCRIPTIONTYPE._serialized_options = b'\x88\xa3\x1e\x00'
    _SUBSCRIPTIONTYPE.values_by_name['TYPE_UNSPECIFIED']._options = None
    _SUBSCRIPTIONTYPE.values_by_name['TYPE_UNSPECIFIED']._serialized_options = b'\x8a\x9d \x0fTypeUnspecified'
    _SUBSCRIPTIONTYPE.values_by_name['TYPE_NODE']._options = None
    _SUBSCRIPTIONTYPE.values_by_name['TYPE_NODE']._serialized_options = b'\x8a\x9d \x08TypeNode'
    _SUBSCRIPTIONTYPE.values_by_name['TYPE_PLAN']._options = None
    _SUBSCRIPTIONTYPE.values_by_name['TYPE_PLAN']._serialized_options = b'\x8a\x9d \x08TypePlan'
    _BASESUBSCRIPTION.fields_by_name['id']._options = None
    _BASESUBSCRIPTION.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _BASESUBSCRIPTION.fields_by_name['expiry_at']._options = None
    _BASESUBSCRIPTION.fields_by_name['expiry_at']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _BASESUBSCRIPTION.fields_by_name['status_at']._options = None
    _BASESUBSCRIPTION.fields_by_name['status_at']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _NODESUBSCRIPTION.fields_by_name['base']._options = None
    _NODESUBSCRIPTION.fields_by_name['base']._serialized_options = b'\xd0\xde\x1f\x01'
    _NODESUBSCRIPTION.fields_by_name['deposit']._options = None
    _NODESUBSCRIPTION.fields_by_name['deposit']._serialized_options = b'\xc8\xde\x1f\x00'
    _PLANSUBSCRIPTION.fields_by_name['base']._options = None
    _PLANSUBSCRIPTION.fields_by_name['base']._serialized_options = b'\xd0\xde\x1f\x01'
    _PLANSUBSCRIPTION.fields_by_name['plan_id']._options = None
    _PLANSUBSCRIPTION.fields_by_name['plan_id']._serialized_options = b'\xe2\xde\x1f\x06PlanID'
    _SUBSCRIPTIONTYPE._serialized_start = 726
    _SUBSCRIPTIONTYPE._serialized_end = 851
    _BASESUBSCRIPTION._serialized_start = 193
    _BASESUBSCRIPTION._serialized_end = 405
    _NODESUBSCRIPTION._serialized_start = 408
    _NODESUBSCRIPTION._serialized_end = 596
    _PLANSUBSCRIPTION._serialized_start = 598
    _PLANSUBSCRIPTION._serialized_end = 724
