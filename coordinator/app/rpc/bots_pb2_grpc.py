# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import bots_pb2 as bots__pb2


class BotManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ping = channel.unary_unary(
                '/BotManager/ping',
                request_serializer=bots__pb2.EmptyMessage.SerializeToString,
                response_deserializer=bots__pb2.Pong.FromString,
                )
        self.call = channel.unary_unary(
                '/BotManager/call',
                request_serializer=bots__pb2.CallToBot.SerializeToString,
                response_deserializer=bots__pb2.BotResponse.FromString,
                )


class BotManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def call(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BotManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ping': grpc.unary_unary_rpc_method_handler(
                    servicer.ping,
                    request_deserializer=bots__pb2.EmptyMessage.FromString,
                    response_serializer=bots__pb2.Pong.SerializeToString,
            ),
            'call': grpc.unary_unary_rpc_method_handler(
                    servicer.call,
                    request_deserializer=bots__pb2.CallToBot.FromString,
                    response_serializer=bots__pb2.BotResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'BotManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BotManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/BotManager/ping',
            bots__pb2.EmptyMessage.SerializeToString,
            bots__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def call(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/BotManager/call',
            bots__pb2.CallToBot.SerializeToString,
            bots__pb2.BotResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class BuildManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ping = channel.unary_unary(
                '/BuildManager/ping',
                request_serializer=bots__pb2.EmptyMessage.SerializeToString,
                response_deserializer=bots__pb2.Pong.FromString,
                )
        self.buildimage = channel.unary_unary(
                '/BuildManager/buildimage',
                request_serializer=bots__pb2.BuildRequest.SerializeToString,
                response_deserializer=bots__pb2.BuildResponse.FromString,
                )


class BuildManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def buildimage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BuildManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ping': grpc.unary_unary_rpc_method_handler(
                    servicer.ping,
                    request_deserializer=bots__pb2.EmptyMessage.FromString,
                    response_serializer=bots__pb2.Pong.SerializeToString,
            ),
            'buildimage': grpc.unary_unary_rpc_method_handler(
                    servicer.buildimage,
                    request_deserializer=bots__pb2.BuildRequest.FromString,
                    response_serializer=bots__pb2.BuildResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'BuildManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BuildManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/BuildManager/ping',
            bots__pb2.EmptyMessage.SerializeToString,
            bots__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def buildimage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/BuildManager/buildimage',
            bots__pb2.BuildRequest.SerializeToString,
            bots__pb2.BuildResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
