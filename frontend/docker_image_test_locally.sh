#!/bin/bash

eval $(minikube docker-env)
docker run -p 5173:5173 xmartlake-front-app:latest
