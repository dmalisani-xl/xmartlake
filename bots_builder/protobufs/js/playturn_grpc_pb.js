// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var playturn_pb = require('./playturn_pb.js');

function serialize_EmptyMessage(arg) {
  if (!(arg instanceof playturn_pb.EmptyMessage)) {
    throw new Error('Expected argument of type EmptyMessage');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_EmptyMessage(buffer_arg) {
  return playturn_pb.EmptyMessage.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_PlayerResponse(arg) {
  if (!(arg instanceof playturn_pb.PlayerResponse)) {
    throw new Error('Expected argument of type PlayerResponse');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_PlayerResponse(buffer_arg) {
  return playturn_pb.PlayerResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Pong(arg) {
  if (!(arg instanceof playturn_pb.Pong)) {
    throw new Error('Expected argument of type Pong');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_Pong(buffer_arg) {
  return playturn_pb.Pong.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_TurnMessage(arg) {
  if (!(arg instanceof playturn_pb.TurnMessage)) {
    throw new Error('Expected argument of type TurnMessage');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_TurnMessage(buffer_arg) {
  return playturn_pb.TurnMessage.deserializeBinary(new Uint8Array(buffer_arg));
}


var TurnCallerService = exports.TurnCallerService = {
  ping: {
    path: '/TurnCaller/ping',
    requestStream: false,
    responseStream: false,
    requestType: playturn_pb.EmptyMessage,
    responseType: playturn_pb.Pong,
    requestSerialize: serialize_EmptyMessage,
    requestDeserialize: deserialize_EmptyMessage,
    responseSerialize: serialize_Pong,
    responseDeserialize: deserialize_Pong,
  },
  play: {
    path: '/TurnCaller/play',
    requestStream: false,
    responseStream: false,
    requestType: playturn_pb.TurnMessage,
    responseType: playturn_pb.PlayerResponse,
    requestSerialize: serialize_TurnMessage,
    requestDeserialize: deserialize_TurnMessage,
    responseSerialize: serialize_PlayerResponse,
    responseDeserialize: deserialize_PlayerResponse,
  },
};

exports.TurnCallerClient = grpc.makeGenericClientConstructor(TurnCallerService);
