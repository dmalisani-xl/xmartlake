import grpc
import bots_pb2
import bots_pb2_grpc

from concurrent import futures
from os import environ

GRPC_PORT = environ.get("GRPC_PORT", 50000)
IMAGE_NAME = environ.get("IMAGE_NAME", "anonymous")


def execute(parameter: str) -> str:
{{code}}


class CallProcess(bots_pb2_grpc.TurnCallerServicer):
    def ping(self, request, context):
        print("Answering PONG")
        response = bots_pb2.Pong(ack="pong")
        return response

    def play(self, request, context) -> str:
        parameter = request.parameter
        print(f"Playing with parameter {parameter}")
        response = execute(parameter)
        return bots_pb2.PlayerResponse(response=response)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    bots_pb2_grpc.add_TurnCallerServicer_to_server(CallProcess(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    server.start()
    print(f"GRPC server running on {IMAGE_NAME}")
    server.wait_for_termination()


if __name__ == "__main__":
    main()