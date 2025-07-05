echo 1
kubectl delete -f ./manifests/
echo 2
docker build -t spec/auth:latest .
echo 3
minikube image load spec/auth:latest
echo 4
kubectl apply -f ./manifests/
echo done