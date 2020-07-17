from seldon_core.proto.prediction_pb2 import SeldonMessage
from io.seldon.protos.PredictionProtos import SeldonMessage as java__SeldonMessage


class SeldonMessageConverter:
    @classmethod
    def to_java(cls, m: java__SeldonMessage) -> SeldonMessage:
        pass
