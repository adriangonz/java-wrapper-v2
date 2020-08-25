import os
import logging
import jpype

logger = logging.getLogger(__name__)


class Baseline:
    def __init__(self):
        logger.debug("[PYTHON] Instantiating MyModel object")
        self._model = None
        self.java__MyModel = None
        self.java__SeldonMessage = None
        self.java__DefaultData = None
        self.java__Tensor = None
        self.java__Arrays = None

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
        self.java__MyModel = jpype.JPackage("io").seldon.demo.MyModel
        self.java__SeldonMessage = jpype.JPackage(
            "io"
        ).seldon.protos.PredictionProtos.SeldonMessage
        self.java__DefaultData = jpype.JPackage(
            "io"
        ).seldon.protos.PredictionProtos.DefaultData
        self.java__Tensor = jpype.JPackage("io").seldon.protos.PredictionProtos.Tensor
        self.java__Arrays = jpype.JPackage("java").util.Arrays

        self._model = self.java__MyModel()

    def predict(self, X, feature_names=[], meta=None):
        logger.debug("[PYTHON] Building message")
        values = self.java__Arrays.asList(X)

        tensor_builder = self.java__Tensor.newBuilder()
        tensor_builder.addShape(X.shape[0])
        tensor_builder.addAllValues(values)
        tensor = tensor_builder.build()

        data_builder = self.java__DefaultData.newBuilder()
        data_builder.setTensor(tensor)
        data = data_builder.build()

        message_builder = self.java__SeldonMessage.newBuilder()
        message_builder.setData(data)
        message = message_builder.build()

        logger.debug("[PYTHON] Sending prediction")
        prediction = self._model.predict(message)

        total = prediction.getData().getTensor().getValues(0)
        return [total]
