# mydjangoapp

## Overview

This project showcases the end-to-end process of creating a Python Django web application, containerizing it with Docker, deploying it to a Minikube Kubernetes cluster, and implementing a Jenkins CI/CD pipeline. The documentation provides step-by-step instructions and commands used in each phase of the project.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Create Python Django Web Application](#step-1-create-python-django-web-application)
- [Step 2: Containerize Python Django Web Application](#step-2-containerize-python-django-web-application)
- [Step 3: Set Up Minikube Kubernetes Cluster](#step-3-set-up-minikube-kubernetes-cluster)
- [Step 4: Deploy Python Django Web Application on Minikube Kubernetes](#step-4-deploy-python-django-web-application-on-minikube-kubernetes)
- [Step 5: Implement Jenkins CI/CD Pipeline](#step-5-implement-jenkins-ci/cd-pipeline)
- [CI/CD Pipeline Workflow](#ci/cd-pipeline-workflow)
- [Monitoring and Logging Setup (Optional)](#monitoring-and-logging-setup-optional)

## Prerequisites

Ensure you have the following software installed:

- [Docker](https://www.docker.com/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Jenkins](https://www.jenkins.io/download/)
- [Git](https://git-scm.com/downloads)

## Step 1: Create Python Django Web Application

### Description:

Create a simple Django web application with a "Hello World" message.

### Commands:

```bash
# Install Django
pip install django

# Create a Django project
django-admin startproject mydjangoapp

# Create a Django app
cd mydjangoapp
python manage.py startapp myapp

# Run the development server
python manage.py runserver
```

## Step 2: Containerize Python Django Web Application

### Description:

Create a Dockerfile to containerize the Django application.

### Dockerfile:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```

### Build and Run:

```bash
# Build the Docker image
docker build -t mydjangoapp .

# Run the Docker container
docker run -p 4000:8000 mydjangoapp
```

## Step 3: Set Up Minikube Kubernetes Cluster

### Description:

Provision a Minikube cluster for local development.

### Commands:

```bash
# Start Minikube cluster
minikube start

# Set kubectl context to Minikube
kubectl config use-context minikube
```

## Step 4: Deploy Python Django Web Application on Minikube Kubernetes

### Description:

Define Kubernetes YAML files for deployment, service, and ingress.

### Files:

#### Deployment (deployment.yaml):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mydjangoapp-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mydjangoapp
  template:
    metadata:
      labels:
        app: mydjangoapp
    spec:
      containers:
      - name: mydjangoapp
        image: mydjangoapp:latest
        ports:
        - containerPort: 8000
```

#### Service (service.yaml):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mydjangoapp-service
spec:
  selector:
    app: mydjangoapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

#### Ingress (ingress.yaml):

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mydjangoapp-ingress
spec:
  rules:
  - host: mydjangoapp.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mydjangoapp-service
            port:
              number: 80
```

### Deployment:

```bash
# Apply Kubernetes configurations
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

## Step 5: Implement Jenkins CI/CD Pipeline

### Description:

Set up Jenkins and configure a CI/CD pipeline to automate Docker builds and Kubernetes deployments.

### Jenkins Pipeline:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build and Push Docker Image') {
            steps {
                script {
                    def dockerImage = "mydjangoapp:${env.BUILD_NUMBER}"
                    docker.build dockerImage
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        docker.image(dockerImage).push()
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    echo "Running tests..."
                    # Add your test commands here
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    def kubeconfig = credentials('kubeconfig-id')
                    withCredentials([file(credentialsId: 'kubeconfig-id', variable: 'KUBECONFIG')]) {
                        sh "kubectl --kubeconfig='${KUBECONFIG}' apply -f deployment.yaml"
                        sh "kubectl --kubeconfig='${KUBECONFIG}' apply -f service.yaml"
                        sh "kubectl --kubeconfig='${KUBECONFIG}' apply -f ingress.yaml"
                    }
                }
            }
        }
    }
}
```

### CI/CD Pipeline Workflow:

1. **Build Docker Image:** Build the Docker image from the Django application code.
2. **Run Tests:** Validate the application's functionality.
3. **Deploy to Minikube:** Deploy the Django application to the Minikube Kubernetes cluster.

## Monitoring and Logging Setup (Optional)

```markdown
# Minikube Monitoring and Logging Setup

## Overview

Guide for setting up monitoring and centralized logging in a Minikube environment. The setup includes the following components:

- **Monitoring:** Utilizing Prometheus for metric collection and Grafana for visualization.
- **Logging:** Implementing centralized logging with Elasticsearch for log storage and Kibana for log visualization.


## Monitoring Setup

### Step 1: Start Minikube

```bash
minikube start
```

### Step 2: Add Helm Repositories

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### Step 3: Install Prometheus and Grafana

```bash
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
helm install grafana grafana/grafana -n monitoring
```

### Step 4: Port-forward Grafana

```bash
kubectl port-forward -n monitoring svc/grafana 3000:80
```

Access Grafana at http://localhost:3000 (default credentials: admin/admin).

## Logging Setup

### Step 1: Install Elasticsearch Operator

```bash
helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace
```

### Step 2: Install Elasticsearch

Create `elasticsearch.yaml`:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: 7.15.2
  nodeSets:
  - name: default
    count: 1
    config:
      node.master: true
      node.data: true
      node.ingest: true
      node.store.allow_mmap: false
```

Apply the custom resource:

```bash
kubectl apply -f elasticsearch.yaml
```

### Step 3: Install Kibana

Create `kibana.yaml`:

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: quickstart
spec:
  version: 7.15.2
  count: 1
  elasticsearchRef:
    name: quickstart
```

Apply the custom resource:

```bash
kubectl apply -f kibana.yaml
```

### Step 4: Port-forward Kibana

```bash
kubectl port-forward -n elastic-system svc/kibana-quickstart-kb-http 5601:5601
```

Access Kibana at http://localhost:5601.

## Clean Up

```bash
minikube stop
minikube delete
```

```





