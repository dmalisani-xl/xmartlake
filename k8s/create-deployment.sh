#!/bin/bash

kubectl apply -f deployment-builder.yml
kubectl apply -f deployment-supervisor.yml
kubectl apply -f deployment-coordinator.yml
