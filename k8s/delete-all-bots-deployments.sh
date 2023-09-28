kubectl get deployments --no-headers=true | awk '/bot-/{print $1}'| xargs  kubectl delete deployment
