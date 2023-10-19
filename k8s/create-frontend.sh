#!/bin/bash

eval $(minikube docker-env)

kubectl delete -f xmartlake-front-app-deployment.yml
kubectl delete -f xmartlake-front-app-service.yml

kubectl apply -f xmartlake-front-app-deployment.yml
kubectl apply -f xmartlake-front-app-service.yml
TIMEOUT_SECONDS=120
INTERVAL_SLEEP=5

pod_name=$(kubectl get pods -l app=xmartlake-front-app -o=jsonpath='{.items[*].metadata.name}')
wait_for_pod_ready() {
    local end_time=$((SECONDS + TIMEOUT_SECONDS))
    echo $SECONDS
    echo $end_time
    while [ $SECONDS -lt $end_time ]; do
        echo "Waiting..."
        sleep $INTERVAL_SLEEP
        echo "Get status"
        pod_status=$(kubectl get pod "$pod_name" -n "$namespace" -o jsonpath='{.status.phase}')
        pod_reason=$(kubectl get pod $pod_name -o jsonpath='{.status.containerStatuses[0].state.waiting.reason}')
        echo "... $SECONDS ---> Current status: $pod_status"
        if [ "$pod_status" == "Running" ]; then
            echo "Pod $pod_name is running and ready!"
            return 0
        elif [ "$pod_reason" == "ErrImageNeverPull" ]; then
            echo "Container image not ready, check build step"
            return 0
        fi
    done
    echo "Timeout: Pod did not become ready within $TIMEOUT_SECONDS seconds."
    return 1
}

wait_for_pod_ready
kubectl port-forward $pod_name 5173:5173
