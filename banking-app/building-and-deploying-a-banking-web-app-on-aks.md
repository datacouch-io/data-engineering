## Building and Deploying a Banking Web App on AKS

### 1. Project Overview

This document outlines the end-to-end process for building a simple, stateless banking web application using Python and Streamlit, containerizing it with Docker, and deploying it to the Azure Kubernetes Service (AKS). The final application will be accessible via a public IP address.

-   Application Framework: Streamlit (Python)
    
-   Containerization: Docker
    
-   Cloud Platform: Microsoft Azure
    
-   Container Registry: Azure Container Registry (ACR)
    
-   Orchestration: Azure Kubernetes Service (AKS)
    

### 2. Prerequisites

Before you begin, ensure you have the following installed and configured:

-   Azure CLI: Authenticated to your Azure account (az login).
    
-   Docker Desktop: Installed and running.
    
-   Python 3: Installed locally.
    
-   VS Code: Or any other code editor.

You also need the following Azure resources. If you don't have them, run these commands:

```
# Create a resource group  
az group  create --name myBankingAppResourceGroup --location  eastus  
  
# Create an Azure Container Registry (ACR)  
az acr create --resource-group  myBankingAppResourceGroup --name mybankingappacr --sku Basic  
  
# Create an Azure Kubernetes Service (AKS) cluster  
az aks create \  
--resource-group  myBankingAppResourceGroup \  
--name myAKSBankingCluster \  
--node-count  1 \  
--enable-addons monitoring \  
--generate-ssh-keys
```

### 3. Step-by-Step Guide

#### Step 1: Application Source Code

Your banking-app project folder should contain the following three files. This section documents their final content for completeness.

You must see these three files listed:
```
banking-app/
├── app.py
├── backend/
│ ├── add_user.py
│ ├── find_user_data.py
│ ├── transfer_money.py
│ └── database.json
├── ui/
│ ├── account_details.py
│ ├── after_log_reg.py
│ ├── home.py
│ ├── login.py
│ ├── online_transactions.py
│ └── register.py
├── deployment.yaml
├── service.yaml
```
#### Step 2: Build and Push the Docker Image

We need to rebuild your Docker image using buildx, which creates an image that works on both your computer and the cloud servers. This single command replaces docker build and docker push.

-   Action: Run this command in your banking-app folder. It will build for the correct platform and push it directly to your ACR.
    
	```
	docker  buildx build --platform linux/amd64 -t mybankingappacr.azurecr.io/banking-app-streamlit:latest . --push
	```
	(Note: This may take a few minutes the first time you run it.)

#### Step 3: Authorize AKS to Access ACR

Run this command to securely link your AKS cluster with your container registry. This is the standard and required way to grant pull permissions.

	
	az aks update --name myAKSBankingCluster --resource-group myBankingAppResourceGroup --attach-acr mybankingappacr

#### Step 4: Deploy Your App to Kubernetes on Azure (AKS) 🚀

These two files define the desired state of your application in Kubernetes.

-   deployment.yaml (Tells AKS how to run your app)
	    
	```
	apiVersion: apps/v1  
	kind: Deployment  
	metadata:  
	name: banking-app-deployment  
	spec:  
	replicas: 2  # Let's run two instances for high availability  
	selector:  
	matchLabels:  
	app: banking-app  
	template:  
	metadata:  
	labels:  
	app: banking-app  
	spec:  
	containers:  
	- name: banking-app-streamlit  
	# This must be the full name of your image in ACR  
	image: mybankingappacr.azurecr.io/banking-app-streamlit:latest  
	ports:  
	- containerPort: 8501  # The port your Streamlit app runs on
	```
-   service.yaml (Exposes your app to the internet)
	    
	```
	apiVersion: v1  
	kind: Service  
	metadata:  
	name: banking-app-service  
	spec:  
	# This creates a public IP address using the Azure Load Balancer  
	type: LoadBalancer  
	selector:  
	# This must match the 'app' label in your deployment  
	app: banking-app  
	ports:  
	- port: 80  # The public port people will access  
	targetPort: 8501  # The port your container is running on
	```
-   Action: Apply these files to your cluster:
    
	```
	kubectl apply -f deployment.yaml  
	kubectl apply -f service.yaml
	```
#### Step 5: Verify and Access Your Application

It can take a minute or two for Azure to create the public IP address for your service.

-   Action: Run this command to watch the status.
    
	```
	kubectl get service banking-app-service --watch
	```
-   Action: Wait until you see an IP address appear in the EXTERNAL-IP column.
    

Open your browser: Copy the external IP address and paste it into your web browser. You should see your "Global Bank Portal" running live from Azure.

### 5. Clean Up Resources

After you've finished the lab, run these commands to delete all the created resources and avoid incurring further costs.

#### Step 1: Delete the Kubernetes Application

This removes the application from your cluster.
```
kubectl delete deployment banking-app-deployment  
kubectl delete service banking-app-service
```
#### Step 2: Delete All Azure Resources

The easiest way to delete all the cloud resources (AKS cluster, ACR, IP addresses, etc.) is to delete the entire resource group.

⚠️ Warning: This action is permanent and cannot be undone.
```
az group delete --name myBankingAppResourceGroup --yes --no-wait
```