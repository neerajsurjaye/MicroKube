echo 1
kubectl delete -f ./manifests/
echo 2
docker build -t spec/converter:latest .
echo 3
minikube image load spec/converter:latest
echo 4
kubectl apply -f ./manifests/
echo done