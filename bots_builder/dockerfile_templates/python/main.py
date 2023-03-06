import grpc
import playturn_pb2
import playturn_pb2_grpc

from concurrent import futures
from os import environ

GRPC_PORT = environ["GRPC_PORT"]
IMAGE_NAME = environ.get("IMAGE_NAME", "anonymous")

class CallProcess(playturn_pb2_grpc.TurnCallerServicer):
    def ping(self, request, context):
        response = playturn_pb2.Pong(ack="pong")
        return response

    def play(parameter: str) -> str:
    {{code}}


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    playturn_pb2_grpc.add_TurnCallerServicer_to_server(CallProcess(), server)
    server.add_insecure_port('[::]:50000')
    server.start()
    print(f"GRPC server running on {IMAGE_NAME}")
    server.wait_for_termination()


if __name__ == "__main__":
    main()