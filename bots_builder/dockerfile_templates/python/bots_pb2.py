# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bots.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nbots.proto\"\x0e\n\x0c\x45mptyMessage\"\x13\n\x04Pong\x12\x0b\n\x03\x61\x63k\x18\x01 \x01(\t\"-\n\tCallToBot\x12\r\n\x05\x62otId\x18\x01 \x01(\t\x12\x11\n\tparameter\x18\x02 \x01(\t\"\x1f\n\x0b\x42otResponse\x12\x10\n\x08response\x18\x01 \x01(\t\"=\n\x0c\x42uildRequest\x12\r\n\x05\x62otId\x18\x01 \x01(\t\x12\x10\n\x08language\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\" \n\rBuildResponse\x12\x0f\n\x07imageId\x18\x01 \x01(\t\" \n\x0bTurnMessage\x12\x11\n\tparameter\x18\x01 \x01(\t\"\"\n\x0ePlayerResponse\x12\x10\n\x08response\x18\x01 \x01(\t2L\n\nBotManager\x12\x1c\n\x04ping\x12\r.EmptyMessage\x1a\x05.Pong\x12 \n\x04\x63\x61ll\x12\n.CallToBot\x1a\x0c.BotResponse2Y\n\x0c\x42uildManager\x12\x1c\n\x04ping\x12\r.EmptyMessage\x1a\x05.Pong\x12+\n\nbuildimage\x12\r.BuildRequest\x1a\x0e.BuildResponse2Q\n\nTurnCaller\x12\x1c\n\x04ping\x12\r.EmptyMessage\x1a\x05.Pong\x12%\n\x04play\x12\x0c.TurnMessage\x1a\x0f.PlayerResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bots_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTYMESSAGE._serialized_start=14
  _EMPTYMESSAGE._serialized_end=28
  _PONG._serialized_start=30
  _PONG._serialized_end=49
  _CALLTOBOT._serialized_start=51
  _CALLTOBOT._serialized_end=96
  _BOTRESPONSE._serialized_start=98
  _BOTRESPONSE._serialized_end=129
  _BUILDREQUEST._serialized_start=131
  _BUILDREQUEST._serialized_end=192
  _BUILDRESPONSE._serialized_start=194
  _BUILDRESPONSE._serialized_end=226
  _TURNMESSAGE._serialized_start=228
  _TURNMESSAGE._serialized_end=260
  _PLAYERRESPONSE._serialized_start=262
  _PLAYERRESPONSE._serialized_end=296
  _BOTMANAGER._serialized_start=298
  _BOTMANAGER._serialized_end=374
  _BUILDMANAGER._serialized_start=376
  _BUILDMANAGER._serialized_end=465
  _TURNCALLER._serialized_start=467
  _TURNCALLER._serialized_end=548
# @@protoc_insertion_point(module_scope)
