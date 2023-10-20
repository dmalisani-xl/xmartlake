builder=$(kubectl get pods -l app=builder -o=jsonpath='{.items[*].metadata.name}')
supervisor=$(kubectl get pods -l app=supervisor -o=jsonpath='{.items[*].metadata.name}')
coordinator=$(kubectl get pods -l app=coordinator -o=jsonpath='{.items[*].metadata.name}')
mongo=$(kubectl get pods -l app=mongo -o=jsonpath='{.items[*].metadata.name}')

front=$(kubectl get pods -l app=xmartlake-front-app -o=jsonpath='{.items[*].metadata.name}')

echo "forwardeo supervisor a ${supervisor}"
kubectl port-forward $supervisor 50050:grpc -n xmartlake &

echo "forwardeo builder $builder"
kubectl port-forward $builder 50051:grpc -n xmartlake &

echo "forwardeo coordinator $coordinator"
kubectl port-forward $coordinator 7000:http -n xmartlake &

echo "forwardeo mongo $mongo"
kubectl port-forward $mongo 27017:mongo-port -n xmartlake &
kubectl port-forward $mongo 8081:mongo-ex-port -n xmartlake &

echo "forwardeo front $front"
kubectl port-forward $front 5173:front -n xmartlake &