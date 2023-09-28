kubectl delete -f deployment-supervisor.yml 
./build_supervisor.sh
kubectl apply -f deployment-supervisor.yml
