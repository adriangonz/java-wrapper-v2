import numpy as np

from seldon_core.proto.prediction_pb2 import SeldonMessage, DefaultData, Tensor

#  from Baseline import Baseline
from ProtobufEncoding import ProtobufEncoding


def main():
    #  model = Baseline()
    model = ProtobufEncoding()

    #  payload = np.array([0.0, 1.1, 2.2, 3.3])
    #  prediction = model.predict(payload)

    message = SeldonMessage(
        data=DefaultData(tensor=Tensor(shape=[1], values=[0.0, 1.1, 2.2, 3.3]))
    )
    prediction = model.predict_raw(message)

    print(f"[PYTHON] Prediction was {prediction}")


if __name__ == "__main__":
    main()
