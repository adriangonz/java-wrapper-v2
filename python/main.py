import numpy as np

from Baseline import Baseline


def main():
    model = Baseline()

    payload = np.array([0.0, 1.1, 2.2, 3.3])
    prediction = model.predict(payload)

    print(f"[PYTHON] Prediction was {prediction}")


if __name__ == "__main__":
    main()
