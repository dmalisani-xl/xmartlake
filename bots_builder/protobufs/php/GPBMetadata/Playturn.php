<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: playturn.proto

namespace GPBMetadata;

class Playturn
{
    public static $is_initialized = false;

    public static function initOnce() {
        $pool = \Google\Protobuf\Internal\DescriptorPool::getGeneratedPool();

        if (static::$is_initialized == true) {
          return;
        }
        $pool->internalAddGeneratedFile(
            '
�
playturn.proto"
EmptyMessage"
Pong
ack (	" 
TurnMessage
	parameter (	""
PlayerResponse
response (	2Q

TurnCaller
ping.EmptyMessage.Pong%
play.TurnMessage.PlayerResponsebproto3'
        , true);

        static::$is_initialized = true;
    }
}

