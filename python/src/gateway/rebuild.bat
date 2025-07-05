echo 1
kubectl delete -f ./manifests/
echo 2
docker build -t spec/gateway:latest .
echo 3
minikube image load spec/gateway:latest
echo 4
kubectl apply -f ./manifests/
echo done