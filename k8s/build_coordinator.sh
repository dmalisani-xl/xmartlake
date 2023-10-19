#!/bin/bash

eval $(minikube docker-env)
docker buildx build ../coordinator -t coordinator:latest
