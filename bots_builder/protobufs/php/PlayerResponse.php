<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: playturn.proto

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * Generated from protobuf message <code>PlayerResponse</code>
 */
class PlayerResponse extends \Google\Protobuf\Internal\Message
{
    /**
     * Generated from protobuf field <code>string response = 1;</code>
     */
    protected $response = '';

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type string $response
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\Playturn::initOnce();
        parent::__construct($data);
    }

    /**
     * Generated from protobuf field <code>string response = 1;</code>
     * @return string
     */
    public function getResponse()
    {
        return $this->response;
    }

    /**
     * Generated from protobuf field <code>string response = 1;</code>
     * @param string $var
     * @return $this
     */
    public function setResponse($var)
    {
        GPBUtil::checkString($var, True);
        $this->response = $var;

        return $this;
    }

}

