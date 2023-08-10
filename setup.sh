#!/bin/bash

# Check if Minikube is already running
minikube status >/dev/null 2>&1

if [[ $? -ne 0 ]]; then
    echo "Minikube is not running. Starting Minikube..."
    minikube start
else
    echo "Minikube is already running."
fi

eval $(minikube -p minikube docker-env)
eval $(minikube docker-env)
minikube cache reload
namespace=xmartlake
kubectl config use-context minikube
kubectl config set-context minikube --namespace=$namespace
kubectl apply -f k8s/namespace.yml

kubectl apply -f k8s/deployment-mongo.yml

kubectl apply -f k8s/deployment-builder.yml
kubectl apply -f k8s/deployment-supervisor.yml
kubectl apply -f k8s/deployment-coordinator.yml
kubectl apply -f k8s/ingress-coordinator.yml
kubectl apply -f k8s/node-reader-role.yaml
kubectl apply -f k8s/node-reader-role-binding.yaml
kubectl apply -f k8s/sevice-builder.yml
kubectl apply -f k8s/service-supervisor.yml
kubectl apply -f k8s/service-coordinator.yml

wait_for_pod_ready() {
    local end_time=$((SECONDS + timeout_seconds))
    echo $SECONDS
    echo $end_time
    while [ $SECONDS -lt $end_time ]; do
        echo $SECONDS
        pod_status=$(kubectl get pod "$pod_name" -n "$namespace" -o jsonpath='{.status.phase}')
        if [ "$pod_status" == "Running" ]; then
            echo "Pod $pod_name is running and ready!"
            return 0
        fi
        sleep $interval_seconds
    done
    echo "Timeout: Pod did not become ready within $timeout_seconds seconds."
    return 1
}

pod_name=$(kubectl get pods -l app=coordinator -o=jsonpath='{.items[*].metadata.name}')

timeout_seconds=120
interval_seconds=5
wait_for_pod_ready

kubectl port-forward $pod_name 7000:http
