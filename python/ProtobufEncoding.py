import os
import logging
import jpype

from seldon_core.proto.prediction_pb2 import SeldonMessage
from seldon_core.user_model import SeldonComponent
from google.protobuf.json_format import ParseDict, MessageToDict

logger = logging.getLogger(__name__)


class ProtobufEncoding(SeldonComponent):
    def __init__(self):
        logger.debug("[PYTHON] Instantiating MyModel object")
        self._model = None
        self._java__MyModel = None

    def load(self):
        """
        We can only have a single JVM per process.
        More details can be found here:
        https://jpype.readthedocs.io/en/latest/userguide.html#multiprocessing
        """
        # TODO: Read JAR path from somewhere
        current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        classpath = os.path.join(current_dir, "java", "build", "libs", "model-all.jar")

        logger.debug(f"[PYTHON] Starting JVM with classpath {classpath}")
        jpype.startJVM(classpath=[classpath])

        # TODO: Make class name configurable
        # Load MyModel class from Java
        java__MyModel = jpype.JPackage("io").seldon.demo.MyModel
        self._model = java__MyModel()

    def predict_raw(self, request) -> SeldonMessage:
        is_proto = True
        if not isinstance(request, SeldonMessage):
            # If `request` is a dict, parse it into a protobuf object
            is_proto = False
            request = ParseDict(request, SeldonMessage())

        logger.debug("[PYTHON] Serialising request")
        serialised = request.SerializeToString()

        logger.debug("[PYTHON] Sending request to Java model")
        prediction_raw = self._model.predict(serialised)

        logger.debug("[PYTHON] De-serialising response")
        response = SeldonMessage()
        response.ParseFromString(bytes(prediction_raw))

        if not is_proto:
            response = MessageToDict(response)

        return response
