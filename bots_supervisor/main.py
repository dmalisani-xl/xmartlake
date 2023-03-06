import grpc
import bots_pb2
import bots_pb2_grpc
from concurrent import futures

class BotManager(bots_pb2_grpc.BotManagerServicer):
    def ping(self, request, context):
        response = bots_pb2.Pong(ack="pong")
        return response

    def call(self, request, context):
        bot_id = request.botId
        parameter = request.parameter
        print("*** Levantar y llamar al bot *** ")
        response = bots_pb2.BotResponse(response="fake_response_of_bot")
        return response

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    bots_pb2_grpc.add_BotManagerServicer_to_server(BotManager(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("GRPC server running on supervisor")
    server.wait_for_termination()

if __name__ == "__main__":
    main()