const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDefinition = protoLoader.loadSync('bots.proto', {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});
const botsProto = grpc.loadPackageDefinition(packageDefinition);

const GRPC_PORT = process.env.GRPC_PORT || '50000';
const IMAGE_NAME = process.env.IMAGE_NAME || 'anonymous';

function execute(parameter) {
    {{code}}
}

const server = new grpc.Server();
  server.addService(botsProto.TurnCaller.service, {
  ping: (call, callback) => {
    console.log('Answering PONG');
    callback(null, { ack: 'pong' });
  },

  play: (call, callback) => {
    const parameter = call.request.parameter;   
    console.log(`Playing with parameter ${parameter}`);
    const response = execute(parameter);
    callback(null, { response: response });
  },
});

server.bindAsync(`0.0.0.0:${GRPC_PORT}`, grpc.ServerCredentials.createInsecure(), () => {
  server.start();
});

console.log(`gRPC server running on ${IMAGE_NAME}`);
