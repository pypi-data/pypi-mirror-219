
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.session.v2 import proof_pb2 as sentinel_dot_session_dot_v2_dot_proof__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsentinel/session/v2/msg.proto\x12\x13sentinel.session.v2\x1a\x14gogoproto/gogo.proto\x1a\x1fsentinel/session/v2/proof.proto"C\n\x0fMsgStartRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12\x12\n\x02id\x18\x02 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x12\x0f\n\x07address\x18\x03 \x01(\t"j\n\x17MsgUpdateDetailsRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12/\n\x05proof\x18\x02 \x01(\x0b2\x1a.sentinel.session.v2.ProofB\x04\xc8\xde\x1f\x00\x12\x11\n\tsignature\x18\x03 \x01(\x0c"@\n\rMsgEndRequest\x12\x0b\n\x03frm\x18\x01 \x01(\t\x12\x12\n\x02id\x18\x02 \x01(\x04B\x06\xe2\xde\x1f\x02ID\x12\x0e\n\x06rating\x18\x03 \x01(\x04"\x12\n\x10MsgStartResponse"\x1a\n\x18MsgUpdateDetailsResponse"\x10\n\x0eMsgEndResponse2\xa9\x02\n\nMsgService\x12W\n\x08MsgStart\x12$.sentinel.session.v2.MsgStartRequest\x1a%.sentinel.session.v2.MsgStartResponse\x12o\n\x10MsgUpdateDetails\x12,.sentinel.session.v2.MsgUpdateDetailsRequest\x1a-.sentinel.session.v2.MsgUpdateDetailsResponse\x12Q\n\x06MsgEnd\x12".sentinel.session.v2.MsgEndRequest\x1a#.sentinel.session.v2.MsgEndResponseB:Z0github.com/sentinel-official/hub/x/session/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.session.v2.msg_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/sentinel-official/hub/x/session/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _MSGSTARTREQUEST.fields_by_name['id']._options = None
    _MSGSTARTREQUEST.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _MSGUPDATEDETAILSREQUEST.fields_by_name['proof']._options = None
    _MSGUPDATEDETAILSREQUEST.fields_by_name['proof']._serialized_options = b'\xc8\xde\x1f\x00'
    _MSGENDREQUEST.fields_by_name['id']._options = None
    _MSGENDREQUEST.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID'
    _MSGSTARTREQUEST._serialized_start = 109
    _MSGSTARTREQUEST._serialized_end = 176
    _MSGUPDATEDETAILSREQUEST._serialized_start = 178
    _MSGUPDATEDETAILSREQUEST._serialized_end = 284
    _MSGENDREQUEST._serialized_start = 286
    _MSGENDREQUEST._serialized_end = 350
    _MSGSTARTRESPONSE._serialized_start = 352
    _MSGSTARTRESPONSE._serialized_end = 370
    _MSGUPDATEDETAILSRESPONSE._serialized_start = 372
    _MSGUPDATEDETAILSRESPONSE._serialized_end = 398
    _MSGENDRESPONSE._serialized_start = 400
    _MSGENDRESPONSE._serialized_end = 416
    _MSGSERVICE._serialized_start = 419
    _MSGSERVICE._serialized_end = 716
