
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n sentinel/deposit/v1/events.proto\x12\x13sentinel.deposit.v1\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x14gogoproto/gogo.proto"\x9b\x01\n\x08EventAdd\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12j\n\x05coins\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB@\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xf2\xde\x1f\x0cyaml:"coins""\xa0\x01\n\rEventSubtract\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12j\n\x05coins\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB@\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xf2\xde\x1f\x0cyaml:"coins"B:Z0github.com/sentinel-official/hub/x/deposit/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.deposit.v1.events_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/sentinel-official/hub/x/deposit/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _EVENTADD.fields_by_name['address']._options = None
    _EVENTADD.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTADD.fields_by_name['coins']._options = None
    _EVENTADD.fields_by_name['coins']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xf2\xde\x1f\x0cyaml:"coins"'
    _EVENTSUBTRACT.fields_by_name['address']._options = None
    _EVENTSUBTRACT.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTSUBTRACT.fields_by_name['coins']._options = None
    _EVENTSUBTRACT.fields_by_name['coins']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xf2\xde\x1f\x0cyaml:"coins"'
    _EVENTADD._serialized_start = 112
    _EVENTADD._serialized_end = 267
    _EVENTSUBTRACT._serialized_start = 270
    _EVENTSUBTRACT._serialized_end = 430
