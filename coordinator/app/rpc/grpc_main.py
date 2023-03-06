import grpc
import bots_pb2
import bots_pb2_grpc


def call_to_bot():
    with grpc.insecure_channel("bots_supervisor:50051") as channel:
        stub = bots_pb2_grpc.BotManagerStub(channel=channel)
        request = bots_pb2.CallToBot(botId="mybot", parameter="XXFFXX")
        response = stub.call(request)
        print(f"Received: {response.response}")
        return response.response

def build_image(bot_id: str, language: str, code: str) -> str:
    with grpc.insecure_channel("bots_builder:50050") as channel:
        stub = bots_pb2_grpc.BuildManagerStub(channel=channel)
        request = bots_pb2.BuildRequest(
            botId=bot_id,
            language=language,
            code=code
        )
        try:
            response = stub.buildimage(request)
            print(f"Received: {response.imageId}")
            return response.imageId
        except Exception as e:
            print(f"Error.: {e}")


def ping_to_builder() -> str:
    with grpc.insecure_channel("bots_builder:50050") as channel:
        stub = bots_pb2_grpc.BuildManagerStub(channel=channel)
        request = bots_pb2.EmptyMessage()
        try:
            response = stub.ping(request)
            print(f"Received: {response.ack}")
            return response.ack
        except Exception as e:
            print(f"Error.: {e}")


def ping_to_manager() -> str:
    with grpc.insecure_channel("bots_supervisor:50051") as channel:
        stub = bots_pb2_grpc.BotManagerStub(channel=channel)
        request = bots_pb2.EmptyMessage()
        try:
            response = stub.ping(request)
            print(f"Received: {response.ack}")
            return response.ack
        except Exception as e:
            print(f"Error.: {e}")