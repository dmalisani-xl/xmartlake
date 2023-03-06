<?php
// GENERATED CODE -- DO NOT EDIT!

namespace ;

/**
 */
class TurnCallerClient extends \Grpc\BaseStub {

    /**
     * @param string $hostname hostname
     * @param array $opts channel options
     * @param \Grpc\Channel $channel (optional) re-use channel object
     */
    public function __construct($hostname, $opts, $channel = null) {
        parent::__construct($hostname, $opts, $channel);
    }

    /**
     * @param \EmptyMessage $argument input argument
     * @param array $metadata metadata
     * @param array $options call options
     * @return \Grpc\UnaryCall
     */
    public function ping(\EmptyMessage $argument,
      $metadata = [], $options = []) {
        return $this->_simpleRequest('/TurnCaller/ping',
        $argument,
        ['\Pong', 'decode'],
        $metadata, $options);
    }

    /**
     * @param \TurnMessage $argument input argument
     * @param array $metadata metadata
     * @param array $options call options
     * @return \Grpc\UnaryCall
     */
    public function play(\TurnMessage $argument,
      $metadata = [], $options = []) {
        return $this->_simpleRequest('/TurnCaller/play',
        $argument,
        ['\PlayerResponse', 'decode'],
        $metadata, $options);
    }

}
