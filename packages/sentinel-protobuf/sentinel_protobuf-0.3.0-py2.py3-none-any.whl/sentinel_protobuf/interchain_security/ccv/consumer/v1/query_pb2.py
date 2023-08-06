
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/interchain_security/ccv/consumer/v1/query.proto\x12#interchain_security.ccv.consumer.v1\x1a\x1cgoogle/api/annotations.proto"\xb2\x01\n\x1bNextFeeDistributionEstimate\x12\x15\n\rcurrentHeight\x18\x01 \x01(\x03\x12\x12\n\nlastHeight\x18\x02 \x01(\x03\x12\x12\n\nnextHeight\x18\x03 \x01(\x03\x12\x1d\n\x15distribution_fraction\x18\x04 \x01(\t\x12\r\n\x05total\x18\x05 \x01(\t\x12\x12\n\ntoProvider\x18\x06 \x01(\t\x12\x12\n\ntoConsumer\x18\x07 \x01(\t")\n\'QueryNextFeeDistributionEstimateRequest"z\n(QueryNextFeeDistributionEstimateResponse\x12N\n\x04data\x18\x01 \x01(\x0b2@.interchain_security.ccv.consumer.v1.NextFeeDistributionEstimate2\x82\x02\n\x05Query\x12\xf8\x01\n\x18QueryNextFeeDistribution\x12L.interchain_security.ccv.consumer.v1.QueryNextFeeDistributionEstimateRequest\x1aM.interchain_security.ccv.consumer.v1.QueryNextFeeDistributionEstimateResponse"?\x82\xd3\xe4\x93\x029\x127/interchain_security/ccv/consumer/next-fee-distributionB<Z:github.com/cosmos/interchain-security/x/ccv/consumer/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'interchain_security.ccv.consumer.v1.query_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z:github.com/cosmos/interchain-security/x/ccv/consumer/types'
    _QUERY.methods_by_name['QueryNextFeeDistribution']._options = None
    _QUERY.methods_by_name['QueryNextFeeDistribution']._serialized_options = b'\x82\xd3\xe4\x93\x029\x127/interchain_security/ccv/consumer/next-fee-distribution'
    _NEXTFEEDISTRIBUTIONESTIMATE._serialized_start = 119
    _NEXTFEEDISTRIBUTIONESTIMATE._serialized_end = 297
    _QUERYNEXTFEEDISTRIBUTIONESTIMATEREQUEST._serialized_start = 299
    _QUERYNEXTFEEDISTRIBUTIONESTIMATEREQUEST._serialized_end = 340
    _QUERYNEXTFEEDISTRIBUTIONESTIMATERESPONSE._serialized_start = 342
    _QUERYNEXTFEEDISTRIBUTIONESTIMATERESPONSE._serialized_end = 464
    _QUERY._serialized_start = 467
    _QUERY._serialized_end = 725
