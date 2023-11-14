# Temperature Data Scraper

## Overview
This project contains a Python script (`scraper.py`) for fetching temperature data from various cities, a Dockerfile for containerizing the application, and Kubernetes deployment configurations for orchestrating the service.

### scraper.py
This Python script fetches temperature data for predefined cities (Zurich, London, Miami, Tokyo, Singapore) using the `requests` library. It sends this data to a Kafka topic using the `confluent_kafka` library.

**Key Features:**
- Fetches temperature data from `wttr.in`.
- Uses Kafka Producer for data transmission.
- Continuous data retrieval with error handling every 5 minutes.

**Key Elements:**
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
```bash
kubectl get pods -n kafka
```
Deploy the Kafka Cluster
```bash
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
**Note on Zookeeper Deployment**
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


### Deployment Instructions

- Build the Docker image: `docker build -t your-registry/kafka-consumer:latest .`
- Push it to your container registry: `docker push your-registry/kafka-consumer:latest`

Create Necessary Credentials:
Create a Kubernetes configMap app-config with Kafka and DB configuration details.
```bash
kubectl create secret generic db-credentials --from-literal=password=<yourpass>
kubectl create configmap app-config --from-literal=host=timescaledb --from-literal=database=temperature --from-literal=user=postgres --from-literal=kafka_bootstrap_servers="my-kafka-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
```

Create a Kubernetes secret db-credentials with the TimescaleDB password.
```bash
kubectl create secret generic timescaledb-secret --from-literal=password=<yourpass>
```

Apply the Kubernetes deployment YAML:
```bash
kubectl apply -f deployment.yaml
```

### Application Flow

#### Scraper App: 
   Collects temperature data and sends it to the Kafka topic temperature-data.
#### Kafka:
   Serves as a message broker, holding the temperature data in the temperature-data topic.
#### Kafka Consumer App:
   Consumes data from the Kafka topic and inserts it into TimescaleDB.
#### TimescaleDB:
Stores the temperature data persistently.This Kafka consumer application acts as a crucial link between real-time data collection and long-term data storage, facilitating efficient data processing and storage workflows.


# Monitoring Kubernetes with Prometheus and Grafana, and Log Management with Loki

## Overview
This guide covers the setup of Prometheus and Grafana for monitoring Kubernetes cluster metrics and Loki along with Promtail for log management. Helm charts are used for installation and configuration of these services.

## Prerequisites
- A Kubernetes cluster
- Helm installed
- `kubectl` command-line tool

## Installation Steps

### 1. Adding Helm Repositories

1. **Add Prometheus Helm Repository:**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update

   Add Grafana Helm Repository:
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

Create a namespace for Prometheus:
```bash
kubectl create namespace prometheus
```

Install Prometheus:
```bash
helm install prometheus prometheus-community/prometheus --namespace prometheus
```


Check the deployed pods:
```bash
kubectl get pods -n prometheus
```

Create a namespace for Grafana:
```bash
kubectl create namespace grafana
```

Install Grafana:
```bash
helm install grafana grafana/grafana --namespace grafana
```

Accessing Grafana Dashboard:
```bash
kubectl port-forward service/grafana 3000:80 -n grafana
```
Access Grafana at http://localhost:3000. Default login is admin and the password can be retrieved by:
```bash
kubectl get secret --namespace grafana grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```


Loki for log aggregation:
```bash
helm install loki grafana/loki-stack --namespace grafana
```

Promtail for shipping logs to Loki:
```bash
helm upgrade --install promtail grafana/promtail --namespace grafana --set loki.serviceName=loki
```

Verify Loki and Promtail Installation:
```bash
kubectl get pods -n grafana
```

 Configuring Grafana to Use Prometheus and Loki
Add Prometheus as a Data Source:
In the Grafana dashboard, navigate to Configuration > Data Sources.
Click "Add data source", and select Prometheus.
Set the URL to http://prometheus-server.prometheus.svc.cluster.local and save.
Add Loki as a Data Source:
Similarly, add Loki as a data source.
Set the URL to http://loki:3100 and save


### Improvement on Deployment

1. Version Control and Branching Strategy
Git for Source Control: Ensure all your Kubernetes configurations, Dockerfiles, and application code are stored in a Git repository.
2. Containerization and Registry
Docker Images: Containerize your applications (Kafka consumer, scraper, etc.) using Docker.
Tag each image with a specific version number corresponding to the Git commit or release version.
3. Deployment with Helm
Helm Charts: Use Helm, a package manager for Kubernetes, to manage deployments. Helm charts should define your application deployment, services, and any dependent resources.
4. Rolling Updates and Rollbacks
Rolling Updates: Kubernetes supports rolling updates natively for Deployments. When you update a Deployment, Kubernetes updates pods with zero downtime.
Automated Rollbacks: Set up criteria for automatic rollbacks in case of failures during updates. 
5. Monitoring and Alerts
Monitoring Tools: Implement monitoring solutions like Prometheus and Grafana to track the health and performance of your applications and Kubernetes cluster.
Alerts: Set up alerts for any critical issues that might require a rollback or immediate attention.
6. CI/CD Pipeline
Continuous Integration (CI): Use a CI tool like Jenkins, GitHub Actions, or GitLab CI to automate the testing of your code and building of Docker images.
Continuous Deployment (CD): Automate deployment with your CI tool. Upon a successful merge to your main branch, the CI tool can update the Docker image, push it to the registry, and update the Helm chart in your Kubernetes cluster.
7. Readiness and Liveness Probes
Probes in Kubernetes: Use readiness and liveness probes in your Kubernetes configurations to ensure that your applications are healthy and ready to serve traffic. If an application fails a liveness probe, Kubernetes can automatically restart the pod.
8. Database Migrations and Data Management
Database Version Control: Use tools like Flyway or Liquibase for database schema version control and migrations.
Backup and Restore: Regularly back up your databases and test restore processes to ensure data integrity and availability.
9. Documentation and Change Management
Documentation: Keep thorough documentation of your deployment processes, configurations, and any manual steps required.
Change Management: Use a change management system to track what was deployed, when, and by whom.
