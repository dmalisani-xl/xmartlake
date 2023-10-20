#!/bin/bash

eval $(minikube docker-env)
docker buildx build . -t xmartlake-front-app:latest
