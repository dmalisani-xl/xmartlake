import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.48.1)",
    comments = "Source: playturn.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class TurnCallerGrpc {

  private TurnCallerGrpc() {}

  public static final String SERVICE_NAME = "TurnCaller";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<Playturn.EmptyMessage,
      Playturn.Pong> getPingMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ping",
      requestType = Playturn.EmptyMessage.class,
      responseType = Playturn.Pong.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<Playturn.EmptyMessage,
      Playturn.Pong> getPingMethod() {
    io.grpc.MethodDescriptor<Playturn.EmptyMessage, Playturn.Pong> getPingMethod;
    if ((getPingMethod = TurnCallerGrpc.getPingMethod) == null) {
      synchronized (TurnCallerGrpc.class) {
        if ((getPingMethod = TurnCallerGrpc.getPingMethod) == null) {
          TurnCallerGrpc.getPingMethod = getPingMethod =
              io.grpc.MethodDescriptor.<Playturn.EmptyMessage, Playturn.Pong>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ping"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  Playturn.EmptyMessage.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  Playturn.Pong.getDefaultInstance()))
              .setSchemaDescriptor(new TurnCallerMethodDescriptorSupplier("ping"))
              .build();
        }
      }
    }
    return getPingMethod;
  }

  private static volatile io.grpc.MethodDescriptor<Playturn.TurnMessage,
      Playturn.PlayerResponse> getPlayMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "play",
      requestType = Playturn.TurnMessage.class,
      responseType = Playturn.PlayerResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<Playturn.TurnMessage,
      Playturn.PlayerResponse> getPlayMethod() {
    io.grpc.MethodDescriptor<Playturn.TurnMessage, Playturn.PlayerResponse> getPlayMethod;
    if ((getPlayMethod = TurnCallerGrpc.getPlayMethod) == null) {
      synchronized (TurnCallerGrpc.class) {
        if ((getPlayMethod = TurnCallerGrpc.getPlayMethod) == null) {
          TurnCallerGrpc.getPlayMethod = getPlayMethod =
              io.grpc.MethodDescriptor.<Playturn.TurnMessage, Playturn.PlayerResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "play"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  Playturn.TurnMessage.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  Playturn.PlayerResponse.getDefaultInstance()))
              .setSchemaDescriptor(new TurnCallerMethodDescriptorSupplier("play"))
              .build();
        }
      }
    }
    return getPlayMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static TurnCallerStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<TurnCallerStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<TurnCallerStub>() {
        @java.lang.Override
        public TurnCallerStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new TurnCallerStub(channel, callOptions);
        }
      };
    return TurnCallerStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static TurnCallerBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<TurnCallerBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<TurnCallerBlockingStub>() {
        @java.lang.Override
        public TurnCallerBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new TurnCallerBlockingStub(channel, callOptions);
        }
      };
    return TurnCallerBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static TurnCallerFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<TurnCallerFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<TurnCallerFutureStub>() {
        @java.lang.Override
        public TurnCallerFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new TurnCallerFutureStub(channel, callOptions);
        }
      };
    return TurnCallerFutureStub.newStub(factory, channel);
  }

  /**
   */
  public static abstract class TurnCallerImplBase implements io.grpc.BindableService {

    /**
     */
    public void ping(Playturn.EmptyMessage request,
        io.grpc.stub.StreamObserver<Playturn.Pong> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPingMethod(), responseObserver);
    }

    /**
     */
    public void play(Playturn.TurnMessage request,
        io.grpc.stub.StreamObserver<Playturn.PlayerResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPlayMethod(), responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            getPingMethod(),
            io.grpc.stub.ServerCalls.asyncUnaryCall(
              new MethodHandlers<
                Playturn.EmptyMessage,
                Playturn.Pong>(
                  this, METHODID_PING)))
          .addMethod(
            getPlayMethod(),
            io.grpc.stub.ServerCalls.asyncUnaryCall(
              new MethodHandlers<
                Playturn.TurnMessage,
                Playturn.PlayerResponse>(
                  this, METHODID_PLAY)))
          .build();
    }
  }

  /**
   */
  public static final class TurnCallerStub extends io.grpc.stub.AbstractAsyncStub<TurnCallerStub> {
    private TurnCallerStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected TurnCallerStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new TurnCallerStub(channel, callOptions);
    }

    /**
     */
    public void ping(Playturn.EmptyMessage request,
        io.grpc.stub.StreamObserver<Playturn.Pong> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getPingMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void play(Playturn.TurnMessage request,
        io.grpc.stub.StreamObserver<Playturn.PlayerResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getPlayMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   */
  public static final class TurnCallerBlockingStub extends io.grpc.stub.AbstractBlockingStub<TurnCallerBlockingStub> {
    private TurnCallerBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected TurnCallerBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new TurnCallerBlockingStub(channel, callOptions);
    }

    /**
     */
    public Playturn.Pong ping(Playturn.EmptyMessage request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getPingMethod(), getCallOptions(), request);
    }

    /**
     */
    public Playturn.PlayerResponse play(Playturn.TurnMessage request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getPlayMethod(), getCallOptions(), request);
    }
  }

  /**
   */
  public static final class TurnCallerFutureStub extends io.grpc.stub.AbstractFutureStub<TurnCallerFutureStub> {
    private TurnCallerFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected TurnCallerFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new TurnCallerFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<Playturn.Pong> ping(
        Playturn.EmptyMessage request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getPingMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<Playturn.PlayerResponse> play(
        Playturn.TurnMessage request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getPlayMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_PING = 0;
  private static final int METHODID_PLAY = 1;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final TurnCallerImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(TurnCallerImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_PING:
          serviceImpl.ping((Playturn.EmptyMessage) request,
              (io.grpc.stub.StreamObserver<Playturn.Pong>) responseObserver);
          break;
        case METHODID_PLAY:
          serviceImpl.play((Playturn.TurnMessage) request,
              (io.grpc.stub.StreamObserver<Playturn.PlayerResponse>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  private static abstract class TurnCallerBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    TurnCallerBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return Playturn.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("TurnCaller");
    }
  }

  private static final class TurnCallerFileDescriptorSupplier
      extends TurnCallerBaseDescriptorSupplier {
    TurnCallerFileDescriptorSupplier() {}
  }

  private static final class TurnCallerMethodDescriptorSupplier
      extends TurnCallerBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    TurnCallerMethodDescriptorSupplier(String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (TurnCallerGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new TurnCallerFileDescriptorSupplier())
              .addMethod(getPingMethod())
              .addMethod(getPlayMethod())
              .build();
        }
      }
    }
    return result;
  }
}
