## 1. Minikube basics
- We will use Docker for Minikube. 

## 2. Install kubectl
```commandline
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x kubectl

sudo mv kubectl /usr/local/bin/
```
## Install Minikube
```commandline
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-latest.x86_64.rpm

sudo rpm -ivh minikube-latest.x86_64.rpm
```
## Start minikube 
- Make sure you have allocated at least 2 cores to your VM on Virtualbox.
```commandline
lscpu | grep Core


# Expected output
Core(s) per socket:    2
Model name:            Intel(R) Core(TM) i7-8750H CPU @ 2.20GHz
```

` minikube start `

- First time it will take time


# kubectl basics

```
kubectl <action, do somethig [apply, delete, get, etc]> <object type> <object id or name> `  
```

## Cluster info 
```
kubectl cluster-info

- Example output
Kubernetes control plane is running at https://192.168.49.2:8443
CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## List nodes
```
kubectl get nodes

- Example output
NAME       STATUS   ROLES                  AGE     VERSION
minikube   Ready    control-plane,master   2m36s   v1.23.3
```
## Create a pod 
` kubectl run firstpod --image=nginx:1.14 --restart=Never ` 

## Connect to a pod 
`kubectl exec -it firstpod -- bash `

## Describe a pod 
` kubectl describe pod firstpod  `

## Delete pod
`  kubectl delete pod firstpod `

## Create a deployment

` kubectl create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.4 `

## Exposing a service as a NodePort

` kubectl expose deployment hello-minikube --type=NodePort --port=8080 `  

or 

` kubectl expose deployment.apps/hello-minikube --type=NodePort --port=8080 ` 

- See all 

```
kubectl get all

NAME                                  READY   STATUS    RESTARTS   AGE
pod/hello-minikube-6ddfcc9757-sdzfh   1/1     Running   0          56s

NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
service/hello-minikube   NodePort    10.100.180.143   <none>        8080:31870/TCP   21s
service/kubernetes       ClusterIP   10.96.0.1        <none>        443/TCP          4m16s

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/hello-minikube   1/1     1            1           57s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/hello-minikube-6ddfcc9757   1         1         1       57s
```

## see the app
- Format  
` curl http://<minikube-cluster-ip>:<service-port> `  

See the page
```
curl http://192.168.49.2:30036

- Example output
CLIENT VALUES:
client_address=172.17.0.1
command=GET
real path=/
query=nil
request_version=1.1
request_uri=http://192.168.49.2:8080/

SERVER VALUES:
server_version=nginx: 1.10.0 - lua: 10001

HEADERS RECEIVED:
accept=*/*
host=192.168.49.2:30036
user-agent=curl/7.29.0
BODY:
-no body in request-
```

## cleanup
```commandline
 kubectl delete deployment hello-minikube
 kubectl delete service hello-minikube
 
 
kubectl get all
 
- Expected output
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   26m
```



## (Optional) Start minikube with options
```
minikube start --help | grep -E 'cpu|memory'
      --cpus='2': Number of CPUs allocated to Kubernetes. Use "max" to use the maximum number of CPUs.
      --memory='': Amount of RAM to allocate to Kubernetes (format: <number>[<unit>], where unit = b, k, m or g). Use "max" to use the maximum amount of memory.
```

## Stop minikube 
` minikube stop `

## Delete minikube 
` minikube delete `


## connecting minikube container
- To connect minikube docker 
```
minikube ssh

docker@minikube:~$ exit
logout
```