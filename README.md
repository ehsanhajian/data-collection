# Temperature Data Scraper

## Overview
This project contains a Python script (`scraper.py`) for fetching temperature data from various cities, a Dockerfile for containerizing the application, and Kubernetes deployment configurations for orchestrating the service.

### Scraper.py
This Python script fetches temperature data for predefined cities (Zurich, London, Miami, Tokyo, Singapore) using the `requests` library. It sends this data to a Kafka topic using the `confluent_kafka` library.

**Key Features:**
- Fetches temperature data from `wttr.in`.
- Uses Kafka Producer for data transmission.
- Continuous data retrieval with error handling.

### Dockerfile
Sets up the environment for running the scraper script in a Docker container.

**Key Elements:**
- Based on Python 3.8 official image.
- Installs `requests` and `confluent-kafka` libraries.
- Configured to execute the scraper script.

### Kubernetes Deployment

**Deployment Features:**
- Single replica deployment.
- Container image from a DigitalOcean registry.
- Resource allocation with requests and limits.

**Horizontal Pod Autoscaler (HPA) Features:**
- Scales between 1 to 10 replicas.
- Target 80% CPU utilization for scaling.

## Deployment to Kubernetes

To deploy this application to a Kubernetes cluster, follow these steps:

1. **Build and Push the Docker Image:**
   - Build the Docker image: `docker build -t your-registry/temperature-scraper:latest .`
   - Push it to your container registry: `docker push your-registry/temperature-scraper:latest`

2. **Apply Kubernetes Configurations:**
   - Ensure you have `kubectl` installed and configured to interact with your Kubernetes cluster.
   - Apply the deployment configuration: `kubectl apply -f deployment.yaml`
   - Apply the HPA configuration: `kubectl apply -f hpa.yaml`

3. **Verify Deployment:**
   - Check the deployment status: `kubectl get deployments`
   - Ensure that pods are running: `kubectl get pods`
   - Monitor HPA status: `kubectl get hpa`

After these steps, the temperature data scraper should be running in your Kubernetes cluster.

# Kafka Cluster Setup in Kubernetes using Helm

## Overview
This guide covers the setup of a Kafka cluster in a Kubernetes environment using the Strimzi operator via Helm. Due to limited resources, Zookeeper is deployed within Kubernetes instead of using a DBaaS solution.

## Prerequisites
- A Kubernetes cluster
- Helm installed
- `kubectl` command-line tool

## Installation Steps

### 1. Setting Up the Strimzi Kafka Operator

**Add the Strimzi Helm Chart Repository:**
   ```bash
   helm repo add strimzi https://strimzi.io/charts/
   ```

** Create a namespace for Kafka:
```bash
kubectl create namespace kafka
```


Install the operator in the kafka namespace:
```bash
helm install strimzi-operator strimzi/strimzi-kafka-operator --namespace kafka
```
Check the operator deployment:
‍‍‍```bash
kubectl get pods -n kafka
```

Deploy the Kafka cluster:
‍‍‍```bash
kubectl apply -f kafka-cluster.yaml -n kafka
```

Check the status of Kafka pods:
```bash
kubectl get pods -n kafka
```

Deploy Kafka Topic:
```bash
kubectl apply -f kafka-topic.yaml -n kafka
```

Check the created topic:
```bash
kubectl get kafkatopics -n kafka
```
Note on Zookeeper Deployment
While deploying Zookeeper as a DBaaS is typically preferred for production environments, in this setup, Zookeeper is deployed within the Kubernetes cluster due to resource limitations. This approach simplifies management but may not be ideal for high-scale production use.

# TimescaleDB Deployment in Kubernetes

## Overview
This guide covers the deployment of TimescaleDB in a Kubernetes environment using a deployment and service configuration.


## Deployment Steps

### 1. Creating Credentials

Before deploying TimescaleDB, you need to create a Kubernetes secret to store the database credentials.

1. **Create a Secret for TimescaleDB Credentials:**
   - You can create a secret using the following command:
     ```bash
     kubectl create secret generic timescaledb-secret --from-literal=password=YOUR_DB_PASSWORD
     ```
   - Replace `YOUR_DB_PASSWORD` with a strong password.

2. **Verify the Secret Creation:**
   - Check the created secret:
     ```bash
     kubectl get secrets
     ```

### 2. TimescaleDB Deployment (timescale-deployment.yaml)


Deploy TimescaleDB:
Apply the deployment configuration:
```bash
kubectl apply -f timescale-deployment.yaml
```

Check the status of the deployment:
```bash
kubectl get deployments
```
Deploy the Service:
```bash
kubectl apply -f timescale-svc.yaml
```
Check the created service:
```bash
kubectl get services
```

# Kafka Consumer Deployment in Kubernetes

## Overview
This Kafka consumer application receives temperature data from a Kafka topic and inserts it into a TimescaleDB database. It acts as an intermediary between the data produced by the scraper app and stored in Kafka, and the TimescaleDB where data is persisted.

## Prerequisites
- A Kafka cluster with a topic named `temperature-data`.
- A TimescaleDB deployment.


### Kafka Consumer Script (kafka-consumer.py)

The `kafka-consumer.py` script consumes messages from a Kafka topic and inserts the data into a TimescaleDB database.


