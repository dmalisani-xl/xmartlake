#!/bin/bash

timeout_seconds=120
echo $SECONDS
sleep 2
end_time=$((SECONDS + timeout_seconds))
echo $SECONDS
echo $end_time
