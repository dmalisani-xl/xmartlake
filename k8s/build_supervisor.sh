#!/bin/bash

eval $(minikube docker-env)
docker buildx build ../bots_supervisor -t supervisor:latest
