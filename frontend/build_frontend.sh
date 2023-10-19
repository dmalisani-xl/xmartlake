#!/bin/bash

eval $(minikube docker-env)
docker buildx build -t xmartlake-front-app:latest .
docker tag xmartlake-front-app:latest xmartlake-front-app:latest
