"""
CLI to generate test benchmark data.
"""
import os
import json
import numpy as np

from typing import List
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.json_format import MessageToDict

from seldon_core.proto.prediction_pb2 import SeldonMessage, DefaultData, Tensor

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")


def generate_test_requests() -> List[SeldonMessage]:
    max_value = 9999
    requests = []

    inputs = max_value * np.random.rand(1024)
    requests.append(
        SeldonMessage(
            data=DefaultData(tensor=Tensor(shape=inputs.shape, values=inputs))
        )
    )
    return requests


def save_grpc_requests(requests: List[SeldonMessage]):
    infer_requests = requests[:1]

    requests_file_path = os.path.join(DATA_PATH, "grpc-requests.pb")
    with open(requests_file_path, "wb") as requests_file:
        for req in infer_requests:
            # To stream multiple messages we need to prefix each one with its
            # size
            # https://ghz.sh/docs/options#-b---binary
            size = req.ByteSize()
            size_varint = _VarintBytes(size)
            requests_file.write(size_varint)

            serialised = req.SerializeToString()
            requests_file.write(serialised)


def save_rest_requests(requests: List[SeldonMessage]):
    # infer_requests_dict = [req.dict() for req in requests]
    # wrk doesn't work with multiple payloads, so take the smallest one.
    # We should consider moving to locust or vegeta.
    infer_requests_dict = MessageToDict(requests[0])
    requests_file_path = os.path.join(DATA_PATH, "rest-requests.json")
    with open(requests_file_path, "w") as requests_file:
        json.dump(infer_requests_dict, requests_file)


def main():
    requests = generate_test_requests()

    save_grpc_requests(requests)
    save_rest_requests(requests)


if __name__ == "__main__":
    main()
