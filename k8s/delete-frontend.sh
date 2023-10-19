#!/bin/bash

eval $(minikube docker-env)

kubectl delete -f xmartlake-front-app-deployment.yml
kubectl delete -f xmartlake-front-app-service.yml
