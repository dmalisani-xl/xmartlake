import os
import grpc
import bots_pb2
import bots_pb2_grpc

from time import sleep

SUPERVISOR_ADDRESS = os.environ["SUPERVISOR_ADDRESS"]
BUILDER_ADDRESS = os.environ["BUILDER_ADDRESS"]


def call_to_bot(bot_id: str, parameter: str):
    with grpc.insecure_channel(SUPERVISOR_ADDRESS) as channel:
        stub = bots_pb2_grpc.BotManagerStub(channel=channel)
        for attempt in [1,2]:
            try:
                request = bots_pb2.CallToBot(botId=bot_id, parameter=parameter)
                break
            except Exception as e:
                print(f"Failed attempt {attempt}")
                print(repr(e))
                sleep(1)
                if attempt == 2:
                    raise Exception(f"Could not contact to bot {bot_id}")

        response = stub.call(request)
        print(f"Received: {response.response}")
        return response.response


def build_image(bot_id: str, language: str, code: str) -> str:
    # TODO: Register bot in mongo
    with grpc.insecure_channel(BUILDER_ADDRESS) as channel:
        stub = bots_pb2_grpc.BuildManagerStub(channel=channel)
        request = bots_pb2.BuildRequest(
            botId=bot_id,
            language=language.value,
            code=code
        )
        try:
            response = stub.buildimage(request)
            print(f"Received: {response.imageId}")
            return response.imageId
        except Exception as e:
            print(f"Error.: {e}")


def ping_to_builder() -> str:
    with grpc.insecure_channel(BUILDER_ADDRESS) as channel:
        stub = bots_pb2_grpc.BuildManagerStub(channel=channel)
        request = bots_pb2.EmptyMessage()
        try:
            response = stub.ping(request)
            print(f"Received: {response.ack}")
            return response.ack
        except Exception as e:
            print(f"Error.: {e}")


def ping_to_manager() -> str:
    with grpc.insecure_channel(SUPERVISOR_ADDRESS) as channel:
        stub = bots_pb2_grpc.BotManagerStub(channel=channel)
        request = bots_pb2.EmptyMessage()
        try:
            response = stub.ping(request)
            print(f"Received: {response.ack}")
            return response.ack
        except Exception as e:
            print(f"Error.: {e}")