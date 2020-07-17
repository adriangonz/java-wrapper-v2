import os
import logging
import jpype

# Point classpath to jar containing all dependencies
# NOTE: This needs to happen before importing our Java modules
current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
classpath = os.path.join(current_dir, "java", "build", "libs", "model-all.jar")
print(f"[PYTHON] Setting classpath as {classpath}")
jpype.startJVM(classpath=[classpath])

# NOTE: Since the `io.` domain is not a standard TLD, we can't use import
java__MyModel = jpype.JPackage("io").seldon.demo.MyModel
java__SeldonMessage = jpype.JPackage("io").seldon.protos.PredictionProtos.SeldonMessage
java__DefaultData = jpype.JPackage("io").seldon.protos.PredictionProtos.DefaultData
java__Tensor = jpype.JPackage("io").seldon.protos.PredictionProtos.Tensor
java__Arrays = jpype.JPackage("java").util.Arrays


logger = logging.getLogger(__name__)


class Baseline:
    def __init__(self):
        logger.debug("[PYTHON] Instantiating MyModel object")
        self._model = java__MyModel()

    def predict(self, X, feature_names=[], meta=None):
        logger.debug("[PYTHON] Building message")
        values = java__Arrays.asList(X)

        tensor_builder = java__Tensor.newBuilder()
        tensor_builder.addShape(X.shape[0])
        tensor_builder.addAllValues(values)
        tensor = tensor_builder.build()

        data_builder = java__DefaultData.newBuilder()
        data_builder.setTensor(tensor)
        data = data_builder.build()

        message_builder = java__SeldonMessage.newBuilder()
        message_builder.setData(data)
        message = message_builder.build()

        logger.debug("[PYTHON] Sending prediction")
        prediction = self._model.predict(message)

        total = prediction.getData().getTensor().getValues(0)
        return [total]
