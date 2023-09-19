eval $(minikube docker-env)
docker buildx build ../bots_builder -t builder:latest
