
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!sentinel/provider/v2/events.proto\x12\x14sentinel.provider.v2\x1a\x14gogoproto/gogo.proto"4\n\rEventRegister\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address""2\n\x0bEventUpdate\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"B;Z1github.com/sentinel-official/hub/x/provider/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.provider.v2.events_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z1github.com/sentinel-official/hub/x/provider/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _EVENTREGISTER.fields_by_name['address']._options = None
    _EVENTREGISTER.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTUPDATE.fields_by_name['address']._options = None
    _EVENTUPDATE.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTREGISTER._serialized_start = 81
    _EVENTREGISTER._serialized_end = 133
    _EVENTUPDATE._serialized_start = 135
    _EVENTUPDATE._serialized_end = 185
