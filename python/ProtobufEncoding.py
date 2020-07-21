import os
import logging
import jpype

from seldon_core.proto.prediction_pb2 import SeldonMessage
from google.protobuf.json_format import ParseDict, MessageToDict

# Point classpath to jar containing all dependencies
# NOTE: This needs to happen before importing our Java modules
current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
classpath = os.path.join(current_dir, "java", "build", "libs", "model-all.jar")
print(f"[PYTHON] Setting classpath as {classpath}")
jpype.startJVM(classpath=[classpath])

# NOTE: Since the `io.` domain is not a standard TLD, we can't use import
java__MyModel = jpype.JPackage("io").seldon.demo.MyModel


logger = logging.getLogger(__name__)


class ProtobufEncoding:
    def __init__(self):
        logger.debug("[PYTHON] Instantiating MyModel object")
        self._model = java__MyModel()

    def predict_raw(self, request) -> SeldonMessage:
        is_proto = True
        if not isinstance(request, SeldonMessage):
            # If `request` is a dict, parse it into a protobuf object
            is_proto = False
            request = ParseDict(request, SeldonMessage())

        serialised = request.SerializeToString()

        prediction_raw = self._model.predict(serialised)

        response = SeldonMessage()
        response.ParseFromString(bytes(prediction_raw))

        if not is_proto:
            response = MessageToDict(response)

        return response
