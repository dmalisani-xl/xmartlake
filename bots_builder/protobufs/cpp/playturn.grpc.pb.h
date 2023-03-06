// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: playturn.proto
#ifndef GRPC_playturn_2eproto__INCLUDED
#define GRPC_playturn_2eproto__INCLUDED

#include "playturn.pb.h"

#include <functional>
#include <grpcpp/impl/codegen/async_generic_service.h>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/client_callback.h>
#include <grpcpp/impl/codegen/client_context.h>
#include <grpcpp/impl/codegen/completion_queue.h>
#include <grpcpp/impl/codegen/message_allocator.h>
#include <grpcpp/impl/codegen/method_handler.h>
#include <grpcpp/impl/codegen/proto_utils.h>
#include <grpcpp/impl/codegen/rpc_method.h>
#include <grpcpp/impl/codegen/server_callback.h>
#include <grpcpp/impl/codegen/server_callback_handlers.h>
#include <grpcpp/impl/codegen/server_context.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/status.h>
#include <grpcpp/impl/codegen/stub_options.h>
#include <grpcpp/impl/codegen/sync_stream.h>

class TurnCaller final {
 public:
  static constexpr char const* service_full_name() {
    return "TurnCaller";
  }
  class StubInterface {
   public:
    virtual ~StubInterface() {}
    virtual ::grpc::Status ping(::grpc::ClientContext* context, const ::EmptyMessage& request, ::Pong* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::Pong>> Asyncping(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::Pong>>(AsyncpingRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::Pong>> PrepareAsyncping(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::Pong>>(PrepareAsyncpingRaw(context, request, cq));
    }
    virtual ::grpc::Status play(::grpc::ClientContext* context, const ::TurnMessage& request, ::PlayerResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::PlayerResponse>> Asyncplay(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::PlayerResponse>>(AsyncplayRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::PlayerResponse>> PrepareAsyncplay(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::PlayerResponse>>(PrepareAsyncplayRaw(context, request, cq));
    }
    class async_interface {
     public:
      virtual ~async_interface() {}
      virtual void ping(::grpc::ClientContext* context, const ::EmptyMessage* request, ::Pong* response, std::function<void(::grpc::Status)>) = 0;
      virtual void ping(::grpc::ClientContext* context, const ::EmptyMessage* request, ::Pong* response, ::grpc::ClientUnaryReactor* reactor) = 0;
      virtual void play(::grpc::ClientContext* context, const ::TurnMessage* request, ::PlayerResponse* response, std::function<void(::grpc::Status)>) = 0;
      virtual void play(::grpc::ClientContext* context, const ::TurnMessage* request, ::PlayerResponse* response, ::grpc::ClientUnaryReactor* reactor) = 0;
    };
    typedef class async_interface experimental_async_interface;
    virtual class async_interface* async() { return nullptr; }
    class async_interface* experimental_async() { return async(); }
   private:
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::Pong>* AsyncpingRaw(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::Pong>* PrepareAsyncpingRaw(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::PlayerResponse>* AsyncplayRaw(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::PlayerResponse>* PrepareAsyncplayRaw(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) = 0;
  };
  class Stub final : public StubInterface {
   public:
    Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());
    ::grpc::Status ping(::grpc::ClientContext* context, const ::EmptyMessage& request, ::Pong* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::Pong>> Asyncping(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::Pong>>(AsyncpingRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::Pong>> PrepareAsyncping(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::Pong>>(PrepareAsyncpingRaw(context, request, cq));
    }
    ::grpc::Status play(::grpc::ClientContext* context, const ::TurnMessage& request, ::PlayerResponse* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::PlayerResponse>> Asyncplay(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::PlayerResponse>>(AsyncplayRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::PlayerResponse>> PrepareAsyncplay(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::PlayerResponse>>(PrepareAsyncplayRaw(context, request, cq));
    }
    class async final :
      public StubInterface::async_interface {
     public:
      void ping(::grpc::ClientContext* context, const ::EmptyMessage* request, ::Pong* response, std::function<void(::grpc::Status)>) override;
      void ping(::grpc::ClientContext* context, const ::EmptyMessage* request, ::Pong* response, ::grpc::ClientUnaryReactor* reactor) override;
      void play(::grpc::ClientContext* context, const ::TurnMessage* request, ::PlayerResponse* response, std::function<void(::grpc::Status)>) override;
      void play(::grpc::ClientContext* context, const ::TurnMessage* request, ::PlayerResponse* response, ::grpc::ClientUnaryReactor* reactor) override;
     private:
      friend class Stub;
      explicit async(Stub* stub): stub_(stub) { }
      Stub* stub() { return stub_; }
      Stub* stub_;
    };
    class async* async() override { return &async_stub_; }

   private:
    std::shared_ptr< ::grpc::ChannelInterface> channel_;
    class async async_stub_{this};
    ::grpc::ClientAsyncResponseReader< ::Pong>* AsyncpingRaw(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::Pong>* PrepareAsyncpingRaw(::grpc::ClientContext* context, const ::EmptyMessage& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::PlayerResponse>* AsyncplayRaw(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::PlayerResponse>* PrepareAsyncplayRaw(::grpc::ClientContext* context, const ::TurnMessage& request, ::grpc::CompletionQueue* cq) override;
    const ::grpc::internal::RpcMethod rpcmethod_ping_;
    const ::grpc::internal::RpcMethod rpcmethod_play_;
  };
  static std::unique_ptr<Stub> NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());

  class Service : public ::grpc::Service {
   public:
    Service();
    virtual ~Service();
    virtual ::grpc::Status ping(::grpc::ServerContext* context, const ::EmptyMessage* request, ::Pong* response);
    virtual ::grpc::Status play(::grpc::ServerContext* context, const ::TurnMessage* request, ::PlayerResponse* response);
  };
  template <class BaseClass>
  class WithAsyncMethod_ping : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_ping() {
      ::grpc::Service::MarkMethodAsync(0);
    }
    ~WithAsyncMethod_ping() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status ping(::grpc::ServerContext* /*context*/, const ::EmptyMessage* /*request*/, ::Pong* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void Requestping(::grpc::ServerContext* context, ::EmptyMessage* request, ::grpc::ServerAsyncResponseWriter< ::Pong>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithAsyncMethod_play : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_play() {
      ::grpc::Service::MarkMethodAsync(1);
    }
    ~WithAsyncMethod_play() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status play(::grpc::ServerContext* /*context*/, const ::TurnMessage* /*request*/, ::PlayerResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void Requestplay(::grpc::ServerContext* context, ::TurnMessage* request, ::grpc::ServerAsyncResponseWriter< ::PlayerResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  typedef WithAsyncMethod_ping<WithAsyncMethod_play<Service > > AsyncService;
  template <class BaseClass>
  class WithCallbackMethod_ping : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithCallbackMethod_ping() {
      ::grpc::Service::MarkMethodCallback(0,
          new ::grpc::internal::CallbackUnaryHandler< ::EmptyMessage, ::Pong>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::EmptyMessage* request, ::Pong* response) { return this->ping(context, request, response); }));}
    void SetMessageAllocatorFor_ping(
        ::grpc::MessageAllocator< ::EmptyMessage, ::Pong>* allocator) {
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::GetHandler(0);
      static_cast<::grpc::internal::CallbackUnaryHandler< ::EmptyMessage, ::Pong>*>(handler)
              ->SetMessageAllocator(allocator);
    }
    ~WithCallbackMethod_ping() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status ping(::grpc::ServerContext* /*context*/, const ::EmptyMessage* /*request*/, ::Pong* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* ping(
      ::grpc::CallbackServerContext* /*context*/, const ::EmptyMessage* /*request*/, ::Pong* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithCallbackMethod_play : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithCallbackMethod_play() {
      ::grpc::Service::MarkMethodCallback(1,
          new ::grpc::internal::CallbackUnaryHandler< ::TurnMessage, ::PlayerResponse>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::TurnMessage* request, ::PlayerResponse* response) { return this->play(context, request, response); }));}
    void SetMessageAllocatorFor_play(
        ::grpc::MessageAllocator< ::TurnMessage, ::PlayerResponse>* allocator) {
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::GetHandler(1);
      static_cast<::grpc::internal::CallbackUnaryHandler< ::TurnMessage, ::PlayerResponse>*>(handler)
              ->SetMessageAllocator(allocator);
    }
    ~WithCallbackMethod_play() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status play(::grpc::ServerContext* /*context*/, const ::TurnMessage* /*request*/, ::PlayerResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* play(
      ::grpc::CallbackServerContext* /*context*/, const ::TurnMessage* /*request*/, ::PlayerResponse* /*response*/)  { return nullptr; }
  };
  typedef WithCallbackMethod_ping<WithCallbackMethod_play<Service > > CallbackService;
  typedef CallbackService ExperimentalCallbackService;
  template <class BaseClass>
  class WithGenericMethod_ping : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_ping() {
      ::grpc::Service::MarkMethodGeneric(0);
    }
    ~WithGenericMethod_ping() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status ping(::grpc::ServerContext* /*context*/, const ::EmptyMessage* /*request*/, ::Pong* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithGenericMethod_play : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_play() {
      ::grpc::Service::MarkMethodGeneric(1);
    }
    ~WithGenericMethod_play() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status play(::grpc::ServerContext* /*context*/, const ::TurnMessage* /*request*/, ::PlayerResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithRawMethod_ping : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_ping() {
      ::grpc::Service::MarkMethodRaw(0);
    }
    ~WithRawMethod_ping() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status ping(::grpc::ServerContext* /*context*/, const ::EmptyMessage* /*request*/, ::Pong* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void Requestping(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithRawMethod_play : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_play() {
      ::grpc::Service::MarkMethodRaw(1);
    }
    ~WithRawMethod_play() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status play(::grpc::ServerContext* /*context*/, const ::TurnMessage* /*request*/, ::PlayerResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void Requestplay(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithRawCallbackMethod_ping : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawCallbackMethod_ping() {
      ::grpc::Service::MarkMethodRawCallback(0,
          new ::grpc::internal::CallbackUnaryHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::grpc::ByteBuffer* request, ::grpc::ByteBuffer* response) { return this->ping(context, request, response); }));
    }
    ~WithRawCallbackMethod_ping() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status ping(::grpc::ServerContext* /*context*/, const ::EmptyMessage* /*request*/, ::Pong* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* ping(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithRawCallbackMethod_play : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawCallbackMethod_play() {
      ::grpc::Service::MarkMethodRawCallback(1,
          new ::grpc::internal::CallbackUnaryHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::grpc::ByteBuffer* request, ::grpc::ByteBuffer* response) { return this->play(context, request, response); }));
    }
    ~WithRawCallbackMethod_play() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status play(::grpc::ServerContext* /*context*/, const ::TurnMessage* /*request*/, ::PlayerResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* play(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_ping : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithStreamedUnaryMethod_ping() {
      ::grpc::Service::MarkMethodStreamed(0,
        new ::grpc::internal::StreamedUnaryHandler<
          ::EmptyMessage, ::Pong>(
            [this](::grpc::ServerContext* context,
                   ::grpc::ServerUnaryStreamer<
                     ::EmptyMessage, ::Pong>* streamer) {
                       return this->Streamedping(context,
                         streamer);
                  }));
    }
    ~WithStreamedUnaryMethod_ping() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status ping(::grpc::ServerContext* /*context*/, const ::EmptyMessage* /*request*/, ::Pong* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status Streamedping(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::EmptyMessage,::Pong>* server_unary_streamer) = 0;
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_play : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithStreamedUnaryMethod_play() {
      ::grpc::Service::MarkMethodStreamed(1,
        new ::grpc::internal::StreamedUnaryHandler<
          ::TurnMessage, ::PlayerResponse>(
            [this](::grpc::ServerContext* context,
                   ::grpc::ServerUnaryStreamer<
                     ::TurnMessage, ::PlayerResponse>* streamer) {
                       return this->Streamedplay(context,
                         streamer);
                  }));
    }
    ~WithStreamedUnaryMethod_play() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status play(::grpc::ServerContext* /*context*/, const ::TurnMessage* /*request*/, ::PlayerResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status Streamedplay(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::TurnMessage,::PlayerResponse>* server_unary_streamer) = 0;
  };
  typedef WithStreamedUnaryMethod_ping<WithStreamedUnaryMethod_play<Service > > StreamedUnaryService;
  typedef Service SplitStreamedService;
  typedef WithStreamedUnaryMethod_ping<WithStreamedUnaryMethod_play<Service > > StreamedService;
};


#endif  // GRPC_playturn_2eproto__INCLUDED
