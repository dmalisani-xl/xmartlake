// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: playturn.proto

#include "playturn.pb.h"
#include "playturn.grpc.pb.h"

#include <functional>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/channel_interface.h>
#include <grpcpp/impl/codegen/client_unary_call.h>
#include <grpcpp/impl/codegen/client_callback.h>
#include <grpcpp/impl/codegen/message_allocator.h>
#include <grpcpp/impl/codegen/method_handler.h>
#include <grpcpp/impl/codegen/rpc_service_method.h>
#include <grpcpp/impl/codegen/server_callback.h>
#include <grpcpp/impl/codegen/server_callback_handlers.h>
#include <grpcpp/impl/codegen/server_context.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/sync_stream.h>

static const char* TurnCaller_method_names[] = {
  "/TurnCaller/ping",
  "/TurnCaller/play",
};

std::unique_ptr< TurnCaller::Stub> TurnCaller::NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options) {
  (void)options;
  std::unique_ptr< TurnCaller::Stub> stub(new TurnCaller::Stub(channel, options));
  return stub;
}

TurnCaller::Stub::Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options)
  : channel_(channel), rpcmethod_ping_(TurnCaller_method_names[0], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_play_(TurnCaller_method_names[1], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  {}

::grpc::Status TurnCaller::Stub::ping(::grpc::ClientContext* context, const ::EmptyMessage& request, ::Pong* response) {
  return ::grpc::internal::BlockingUnaryCall< ::EmptyMessage, ::Pong, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_ping_, context, request, response);
}

void TurnCaller::Stub::async::ping(::grpc::ClientContext* context, const ::EmptyMessage* request, ::Pong* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::EmptyMessage, ::Pong, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_ping_, context, request, response, std::move(f));
}

void TurnCaller::Stub::async::ping(::grpc::ClientContext* context, const ::EmptyMessage* request, ::Pong* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_ping_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::Pong>* TurnCaller::Stub::PrepareAsyncpingRaw(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::Pong, ::EmptyMessage, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_ping_, context, request);
}

::grpc::ClientAsyncResponseReader< ::Pong>* TurnCaller::Stub::AsyncpingRaw(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncpingRaw(context, request, cq);
  result->StartCall();
  return result;
}

::grpc::Status TurnCaller::Stub::play(::grpc::ClientContext* context, const ::TurnMessage& request, ::PlayerResponse* response) {
  return ::grpc::internal::BlockingUnaryCall< ::TurnMessage, ::PlayerResponse, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_play_, context, request, response);
}

void TurnCaller::Stub::async::play(::grpc::ClientContext* context, const ::TurnMessage* request, ::PlayerResponse* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::TurnMessage, ::PlayerResponse, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_play_, context, request, response, std::move(f));
}

void TurnCaller::Stub::async::play(::grpc::ClientContext* context, const ::TurnMessage* request, ::PlayerResponse* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_play_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::PlayerResponse>* TurnCaller::Stub::PrepareAsyncplayRaw(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::PlayerResponse, ::TurnMessage, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_play_, context, request);
}

::grpc::ClientAsyncResponseReader< ::PlayerResponse>* TurnCaller::Stub::AsyncplayRaw(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncplayRaw(context, request, cq);
  result->StartCall();
  return result;
}

TurnCaller::Service::Service() {
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      TurnCaller_method_names[0],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< TurnCaller::Service, ::EmptyMessage, ::Pong, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](TurnCaller::Service* service,
             ::grpc::ServerContext* ctx,
             const ::EmptyMessage* req,
             ::Pong* resp) {
               return service->ping(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      TurnCaller_method_names[1],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< TurnCaller::Service, ::TurnMessage, ::PlayerResponse, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](TurnCaller::Service* service,
             ::grpc::ServerContext* ctx,
             const ::TurnMessage* req,
             ::PlayerResponse* resp) {
               return service->play(ctx, req, resp);
             }, this)));
}

TurnCaller::Service::~Service() {
}

::grpc::Status TurnCaller::Service::ping(::grpc::ServerContext* context, const ::EmptyMessage* request, ::Pong* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status TurnCaller::Service::play(::grpc::ServerContext* context, const ::TurnMessage* request, ::PlayerResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


