````markdown
# 🚀 Deploying Apache Spark on Kubernetes

This project shows you how to deploy Apache Spark on a local Kubernetes cluster using Minikube.

---

## 🔧 Want to Learn How to Build This?

You're in the right place! Follow the steps below to build and run this project.

---

## ▶️ Want to Use This Project?

### 📦 Minikube Setup

To run this project locally, install and configure the following tools:

1. **[Hypervisor](https://kubernetes.io/docs/tasks/tools/install-minikube/#install-a-hypervisor)**  
   Use [VirtualBox](https://www.virtualbox.org/wiki/Downloads), [HyperKit](https://github.com/moby/hyperkit), or another hypervisor supported by your OS.

2. **[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)**  
   Required for interacting with your Kubernetes cluster.

3. **[Minikube](https://github.com/kubernetes/minikube/releases)**  
   Local Kubernetes for development and testing.

---

### 🖥️ Start the Minikube Cluster

```bash
minikube start --memory 8192 --cpus 4
minikube dashboard
````

---

### 🐳 Build the Docker Image

```bash
eval $(minikube docker-env)
chmod +x docker/common.sh docker/spark-master docker/spark-worker
docker build -t spark-python:3.5.6 -f ./docker/Dockerfile ./docker
```

---

### ☸️ Create Deployments and Services

```bash
kubectl create -f ./kubernetes/spark-master-deployment.yaml
kubectl create -f ./kubernetes/spark-master-service.yaml
kubectl create -f ./kubernetes/spark-worker-deployment.yaml
```

---

### 🌐 Enable Ingress & Create Rule

```bash
minikube addons enable ingress
kubectl apply -f ./kubernetes/minikube-ingress.yaml
```

---

### 🧭 Update `/etc/hosts` for Local Access

```bash
echo "$(minikube ip) spark.local" | sudo tee -a /etc/hosts
```

✅ Ensure the file contains an entry like:

```
192.168.49.2 spark.local
```

---

## 🧪 Submit a PySpark Job

### Get the Spark Master Pod Name

```bash
kubectl get pods -l component=spark-master
```

### Open a Shell into the Pod

```bash
kubectl exec -it <spark-master-pod-name> -- bash
```

### Run the Spark Submit Command

```bash
/opt/spark/bin/spark-submit \
  --master spark://spark-master-svc:7077 \
  --deploy-mode client \
  --name demo-k8s-job \
  --num-executors 4 \
  --executor-memory 512m \
  --executor-cores 1 \
  /opt/spark/sample.py
```

---

## 🌍 Access the Spark UI

Visit the Spark Master UI at:
👉 [http://spark.local](http://spark.local)

---

## 📁 Folder Structure Overview

```
.
├── docker/
│   ├── Dockerfile
│   ├── common.sh
│   ├── spark-master
│   ├── spark-worker
│   └── sample.py
├── kubernetes/
│   ├── spark-master-deployment.yaml
│   ├── spark-master-service.yaml
│   ├── spark-worker-deployment.yaml
│   └── minikube-ingress.yaml
└── README.md
----
```
