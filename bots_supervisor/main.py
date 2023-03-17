import os
import grpc
import logging
import sys
import bots_pb2
import bots_pb2_grpc
from concurrent import futures
from bots_manager.main import call_to_bot

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

GRPC_PORT = os.environ["GRPC_PORT"]
class BotManager(bots_pb2_grpc.BotManagerServicer):
    def ping(self, request, context):
        response = bots_pb2.Pong(ack="pong")
        return response

    def call(self, request, context):
        bot_id = request.botId
        parameter = request.parameter
        response_of_bot = call_to_bot(bot_id=bot_id, parameter=parameter)
        response = bots_pb2.BotResponse(response=response_of_bot)
        return response

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    bots_pb2_grpc.add_BotManagerServicer_to_server(BotManager(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    server.start()
    print(f"GRPC server running on supervisor. Port: {GRPC_PORT}")
    server.wait_for_termination()

if __name__ == "__main__":
    main()