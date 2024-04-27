In this project we will deploy ml models on Docker and Kubernetes.
```commandline
mv 12_deploy_fastapi_on_docker_k8s/ 12
cd 12
```
## 1. Go to kubernetes_notes

## 2. Deploy on Docker

### 2.1. Build image
```commandline
eval $(minikube docker-env)

docker image build -t ml-prediction-with-fastapi:1.0 .
```
### 2.2. Run container
```commandline
docker run --rm \
--name ml-prediction \
-p 8002:8000 -d ml-prediction-with-fastapi:1.0
```

### 2.3. Prediction
```commandline
curl -X 'POST' \
  'http://127.0.0.1:8002/prediction/iris' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "SepalLengthCm": 5.1,
  "SepalWidthCm": 3.5,
  "PetalLengthCm": 1.4,
  "PetalWidthCm": 0.2
}'
```
- Expected output: `"Iris-setosa"`

### 2.4. Stop docker container 
` docker container stop  ml-prediction `  

- More information: https://fastapi.tiangolo.com/deployment/docker/


## 3. Minikube
```commandline
kubectl apply -f ml-prediction-deployment.yaml
```
### 3.1. Create service
```commandline
kubectl create service nodeport ml-prediction --tcp=8000:8000
kubectl get services


NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
kubernetes      ClusterIP   10.96.0.1      <none>        443/TCP          6h24m
ml-prediction   NodePort    10.99.159.87   <none>        8000:31647/TCP   72s
```

## 4. Prediction on Minikube NodePort
```commandline
curl -X 'POST' \
  'http://192.168.49.2:30833/prediction/iris' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "SepalLengthCm": 5.1,
  "SepalWidthCm": 3.5,
  "PetalLengthCm": 1.4,
  "PetalWidthCm": 0.2
}'
```
- Expected output:  
` "Iris-setosa" `

## 5. Ingress
```commandline
minikube addons enable ingress

kubectl apply -f ingress-ml-prediction.yaml
 
sudo vim /etc/hosts
192.168.49.2    ml.prediction.vbo.local
```
```commandline
curl -X 'POST' \
  'ml.prediction.vbo.local/prediction/iris' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "SepalLengthCm": 5.1,
  "SepalWidthCm": 3.5,
  "PetalLengthCm": 1.4,
  "PetalWidthCm": 0.2
}'
```

- Expected output  
` "Iris-setosa" `

## Use NGINX for UI
