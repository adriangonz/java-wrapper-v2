#  import numpy as np

from seldon_core.proto.prediction_pb2 import SeldonMessage, DefaultData, Tensor
from google.protobuf.json_format import MessageToJson

from NoJava import NoJava

#  from Baseline import Baseline
#  from ProtobufEncoding import ProtobufEncoding
from PayloadPassthrough import PayloadPassthrough


def main():
    model = NoJava()
    #  model = Baseline()
    #  model = ProtobufEncoding()
    model = PayloadPassthrough()

    model.load()

    #  payload = np.array([0.0, 1.1, 2.2, 3.3])
    #  prediction = model.predict(payload)

    #  message = SeldonMessage(
    #  data=DefaultData(tensor=Tensor(shape=[1], values=[0.0, 1.1, 2.2, 3.3]))
    #  )
    #  prediction = model.predict_raw(message)

    for n in range(100000):
        message = SeldonMessage(
            data=DefaultData(tensor=Tensor(shape=[1], values=[0.0, 1.1, 2.2, 3.3]))
        )
        prediction = model.predict_raw(MessageToJson(message))

        print(f"[PYTHON] Prediction was {prediction}")


if __name__ == "__main__":
    main()
