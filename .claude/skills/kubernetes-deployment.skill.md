# Kubernetes Deployment Skill

## Purpose
This skill describes how to deploy the Todo application on Kubernetes with Dapr and event-driven architecture.

## When to Use
- When deploying to Minikube locally
- When deploying to cloud Kubernetes (AKS/GKE)
- When setting up production environments
- When implementing CI/CD pipelines
- When configuring autoscaling

## Prerequisites
- Kubernetes cluster (Minikube, AKS, GKE, etc.)
- Dapr installed on the cluster
- Helm for package management
- kubectl for cluster management

## Installation Steps
1. Install Dapr on Kubernetes
```bash
dapr init -k
```

2. Deploy Dapr components
```bash
kubectl apply -f dapr-components/
```

3. Create Kubernetes manifests
4. Deploy applications with Dapr sidecars

## Kubernetes Manifests
### Deployment with Dapr Sidecar
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  labels:
    app: todo-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
        dapr.io/config: "app-config"
    spec:
      containers:
      - name: todo-backend
        image: todo-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
spec:
  selector:
    app: todo-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

### Kafka Deployment (using Strimzi)
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: taskflow-kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
        deleteClaim: false
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

## Helm Chart Structure
```
helm-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl
│   └── dapr-components/
│       ├── pubsub.yaml
│       ├── statestore.yaml
│       └── secrets.yaml
└── charts/
```

## Deployment Commands
```bash
# Package the Helm chart
helm package helm-chart/

# Deploy to cluster
helm install todo-app helm-chart/ --values values.yaml

# Upgrade deployment
helm upgrade todo-app helm-chart/ --values values.yaml

# Check deployment status
helm status todo-app
```

## Health Checks and Monitoring
- Liveness and readiness probes
- Resource limits and requests
- Horizontal pod autoscaler
- Service mesh integration
- Observability stack (Prometheus, Grafana)

## Security Considerations
- Network policies
- RBAC configuration
- TLS encryption
- Secret management
- Pod security policies