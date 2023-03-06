// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: playturn.proto

// This CPP symbol can be defined to use imports that match up to the framework
// imports needed when using CocoaPods.
#if !defined(GPB_USE_PROTOBUF_FRAMEWORK_IMPORTS)
 #define GPB_USE_PROTOBUF_FRAMEWORK_IMPORTS 0
#endif

#if GPB_USE_PROTOBUF_FRAMEWORK_IMPORTS
 #import <Protobuf/GPBProtocolBuffers.h>
#else
 #import "GPBProtocolBuffers.h"
#endif

#if GOOGLE_PROTOBUF_OBJC_VERSION < 30004
#error This file was generated by a newer version of protoc which is incompatible with your Protocol Buffer library sources.
#endif
#if 30004 < GOOGLE_PROTOBUF_OBJC_MIN_SUPPORTED_VERSION
#error This file was generated by an older version of protoc which is incompatible with your Protocol Buffer library sources.
#endif

// @@protoc_insertion_point(imports)

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wdeprecated-declarations"

CF_EXTERN_C_BEGIN

NS_ASSUME_NONNULL_BEGIN

#pragma mark - PlayturnRoot

/**
 * Exposes the extension registry for this file.
 *
 * The base class provides:
 * @code
 *   + (GPBExtensionRegistry *)extensionRegistry;
 * @endcode
 * which is a @c GPBExtensionRegistry that includes all the extensions defined by
 * this file and all files that it depends on.
 **/
GPB_FINAL @interface PlayturnRoot : GPBRootObject
@end

#pragma mark - EmptyMessage

GPB_FINAL @interface EmptyMessage : GPBMessage

@end

#pragma mark - Pong

typedef GPB_ENUM(Pong_FieldNumber) {
  Pong_FieldNumber_Ack = 1,
};

GPB_FINAL @interface Pong : GPBMessage

@property(nonatomic, readwrite, copy, null_resettable) NSString *ack;

@end

#pragma mark - TurnMessage

typedef GPB_ENUM(TurnMessage_FieldNumber) {
  TurnMessage_FieldNumber_Parameter = 1,
};

GPB_FINAL @interface TurnMessage : GPBMessage

@property(nonatomic, readwrite, copy, null_resettable) NSString *parameter;

@end

#pragma mark - PlayerResponse

typedef GPB_ENUM(PlayerResponse_FieldNumber) {
  PlayerResponse_FieldNumber_Response = 1,
};

GPB_FINAL @interface PlayerResponse : GPBMessage

@property(nonatomic, readwrite, copy, null_resettable) NSString *response;

@end

NS_ASSUME_NONNULL_END

CF_EXTERN_C_END

#pragma clang diagnostic pop

// @@protoc_insertion_point(global_scope)
