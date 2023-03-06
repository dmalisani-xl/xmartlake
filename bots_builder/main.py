import os
import sys
import grpc
import bots_pb2
import bots_pb2_grpc
import docker
import base64
import logging
from concurrent import futures
from base_reference import source_info

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

docker_client = docker.from_env()


def put_code_on_file(language: str, code_b64: str):
    with open(source_info[language]['main_file'], "r+") as f:
        logger.debug("Open file")
        entire_file = f.read()
        f.seek(0)
        logger.debug("Changing content")
        code = base64.b64decode(code_b64).decode()
        changed = entire_file.replace("{{code}}", code)
        logger.debug("File changed")
        f.write(changed)


def build_image(language: str, tag: str):
    logger.debug(f"Start to build image {tag}")
    a, _ = docker_client.images.build(
        path=source_info[language]['base_path'],
        tag=tag
    )
    return a.id



def make_new_image(*, bot_id: str, language: str, code_b64: str) -> str:
    logger.info(f"Building image for {bot_id}")
    put_code_on_file(language, code_b64)
    return build_image(language=language, tag=bot_id)


class Building(bots_pb2_grpc.BuildManager):
    def ping(self, request, context):
        response = bots_pb2.Pong(ack="pong")
        return response

    def buildimage(self, request, context):
        logger.info(f"request received {request}")
        bot_id = request.botId
        language = request.language
        code = request.code
        result = make_new_image(bot_id=bot_id, language=language, code_b64=code)
        print(f"Result: {result}")
        response = bots_pb2.BuildResponse(imageId=result)
        return response


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    bots_pb2_grpc.add_BuildManagerServicer_to_server(Building(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    print("GRPC server running on builder")
    server.wait_for_termination()

if __name__ == "__main__":
    main()