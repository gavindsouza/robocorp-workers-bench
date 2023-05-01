#!/bin/sh

echo "Linking the Agent with name $NAME and token $LINK_TOKEN"
./bin/robocorp-workforce-agent-core link $LINK_TOKEN --name $NAME --instance-path /home/worker/instance
echo "Linking succeeded"

echo "Starting the Agent..."
./bin/robocorp-workforce-agent-core start --instance-path /home/worker/instance

