minikube start
eval $(minikube -p minikube docker-env)

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
