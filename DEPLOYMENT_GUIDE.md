# 🚀 PILOTFORGEAI Deployment Guide

Complete guide for deploying PILOTFORGEAI in various environments.

---

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Checklist](#production-checklist)
5. [Monitoring & Logging](#monitoring--logging)
6. [Troubleshooting](#troubleshooting)

---

## 🖥️ Local Development

### Prerequisites
- Python 3.11 or 3.12
- 4GB RAM minimum (8GB recommended)
- 2GB disk space

### Setup
```bash
# Clone repository
git clone https://github.com/hneal055/EnhancedBudgetPro.git
cd EnhancedBudgetPro

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python validate_system.py
```

### Run Locally
```bash
# Streamlit UI (Port 8501)
streamlit run ui_app.py

# Flask Web App (Port 5000)
python web_app.py

# CLI
python -m src.cli analyze --input samples/test_script.fdx --out ./output
```

---

## �� Docker Deployment

### Build Docker Image

```bash
# Build from Dockerfile
docker build -t pilotforgeai:latest .

# Verify image
docker images | grep pilotforge
```

### Run Container

#### Streamlit UI
```bash
docker run -d \
  --name pilotforge-ui \
  -p 8501:8501 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/samples:/app/samples:ro \
  --restart unless-stopped \
  pilotforgeai:latest

# Access: http://localhost:8501
```

#### Flask Web App
```bash
docker run -d \
  --name pilotforge-web \
  -p 5000:5000 \
  -v $(pwd)/web_output:/app/web_output \
  -v $(pwd)/samples:/app/samples:ro \
  --restart unless-stopped \
  pilotforgeai:latest python web_app.py

# Access: http://localhost:5000
```

#### GPU Support
```bash
docker run -d \
  --gpus all \
  --name pilotforge-gpu \
  -p 8501:8501 \
  -v $(pwd)/output:/app/output \
  pilotforgeai:latest

# Check GPU: docker logs pilotforge-gpu
```

### Docker Compose (Multi-Service)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up -d --build
```

**Services**:
- Streamlit UI: http://localhost:8501
- Flask Web: http://localhost:5000

---

## ☁️ Cloud Deployment

### AWS Deployment

#### AWS ECS (Elastic Container Service)

1. **Push to ECR**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag pilotforgeai:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/pilotforgeai:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/pilotforgeai:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "pilotforgeai-task",
  "containerDefinitions": [
    {
      "name": "pilotforge-streamlit",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/pilotforgeai:latest",
      "cpu": 512,
      "memory": 1024,
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "STREAMLIT_SERVER_PORT",
          "value": "8501"
        }
      ]
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "512",
  "memory": "1024"
}
```

3. **Create ECS Service**
```bash
aws ecs create-service \
  --cluster pilotforge-cluster \
  --service-name pilotforge-service \
  --task-definition pilotforgeai-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

#### AWS Lambda (Serverless)

```bash
# Package for Lambda
pip install -t ./package -r requirements.txt
cd package && zip -r ../deployment.zip . && cd ..
zip -g deployment.zip src/ -r

# Create Lambda function
aws lambda create-function \
  --function-name pilotforge-analyzer \
  --runtime python3.12 \
  --role arn:aws:iam::<account-id>:role/lambda-role \
  --handler lambda_function.handler \
  --zip-file fileb://deployment.zip \
  --timeout 300 \
  --memory-size 2048
```

### Azure Deployment

#### Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name pilotforge-rg --location eastus

# Deploy container
az container create \
  --resource-group pilotforge-rg \
  --name pilotforge-aci \
  --image hneal055/pilotforgeai:latest \
  --dns-name-label pilotforge \
  --ports 8501 \
  --cpu 2 \
  --memory 4

# Get FQDN
az container show \
  --resource-group pilotforge-rg \
  --name pilotforge-aci \
  --query ipAddress.fqdn
```

#### Azure App Service

```bash
# Create App Service plan
az appservice plan create \
  --name pilotforge-plan \
  --resource-group pilotforge-rg \
  --is-linux \
  --sku B1

# Create web app
az webapp create \
  --resource-group pilotforge-rg \
  --plan pilotforge-plan \
  --name pilotforge-app \
  --deployment-container-image-name hneal055/pilotforgeai:latest

# Configure port
az webapp config appsettings set \
  --resource-group pilotforge-rg \
  --name pilotforge-app \
  --settings WEBSITES_PORT=8501
```

### Google Cloud Platform

#### GCP Cloud Run

```bash
# Login
gcloud auth login

# Deploy to Cloud Run
gcloud run deploy pilotforge \
  --image hneal055/pilotforgeai:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501 \
  --memory 2Gi \
  --cpu 2

# Get service URL
gcloud run services describe pilotforge \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

#### GCP Kubernetes Engine (GKE)

```bash
# Create cluster
gcloud container clusters create pilotforge-cluster \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type e2-standard-2

# Deploy
kubectl create deployment pilotforge \
  --image=hneal055/pilotforgeai:latest

# Expose service
kubectl expose deployment pilotforge \
  --type=LoadBalancer \
  --port=80 \
  --target-port=8501

# Get external IP
kubectl get service pilotforge
```

---

## ✅ Production Checklist

### Security
- [ ] Change default passwords/secrets
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up API authentication
- [ ] Enable rate limiting
- [ ] Review CORS settings
- [ ] Scan for vulnerabilities (Trivy)
- [ ] Set up WAF (Web Application Firewall)

### Performance
- [ ] Configure autoscaling
- [ ] Set up CDN for static assets
- [ ] Enable caching (Redis/Memcached)
- [ ] Optimize database queries
- [ ] Configure load balancing
- [ ] Enable GPU acceleration (if available)
- [ ] Set resource limits (CPU/memory)
- [ ] Monitor response times

### Reliability
- [ ] Set up health checks
- [ ] Configure automatic restarts
- [ ] Implement backup strategy
- [ ] Set up disaster recovery
- [ ] Configure monitoring alerts
- [ ] Test failover scenarios
- [ ] Document incident response
- [ ] Set up redundancy

### Monitoring
- [ ] Application logs (CloudWatch/Stackdriver)
- [ ] Performance metrics (Prometheus/Grafana)
- [ ] Error tracking (Sentry)
- [ ] Uptime monitoring (Pingdom/UptimeRobot)
- [ ] User analytics
- [ ] Cost monitoring
- [ ] Security audit logs

### Compliance
- [ ] Review data privacy (GDPR/CCPA)
- [ ] Set up data retention policies
- [ ] Enable audit logging
- [ ] Review license compliance
- [ ] Document API endpoints
- [ ] Terms of Service
- [ ] Privacy Policy

---

## 📊 Monitoring & Logging

### Application Logs

```bash
# Docker logs
docker logs -f pilotforge-ui

# With timestamp
docker logs -f --since 1h pilotforge-ui

# Export logs
docker logs pilotforge-ui > app.log
```

### Health Checks

```bash
# Streamlit health
curl http://localhost:8501/_stcore/health

# Flask health (add endpoint to web_app.py)
curl http://localhost:5000/health
```

### Metrics Collection

```python
# Add to application
from prometheus_client import Counter, Histogram

request_count = Counter('pilotforge_requests_total', 'Total requests')
request_duration = Histogram('pilotforge_request_duration_seconds', 'Request duration')
```

### Log Aggregation

```yaml
# Fluent Bit configuration
[INPUT]
    Name tail
    Path /var/log/pilotforge/*.log
    Tag pilotforge

[OUTPUT]
    Name cloudwatch
    Match pilotforge
    region us-east-1
    log_group_name /aws/pilotforge
```

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check container status
docker ps -a

# View logs
docker logs pilotforge-ui

# Inspect container
docker inspect pilotforge-ui

# Common issues:
# 1. Port already in use: Change -p 8501:8501 to -p 8502:8501
# 2. Volume mount error: Check path exists
# 3. Permission denied: Add --user $(id -u):$(id -g)
```

### GPU Not Detected

```bash
# Check NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Out of Memory

```bash
# Increase container memory
docker run -d \
  --name pilotforge-ui \
  --memory="4g" \
  --memory-swap="4g" \
  -p 8501:8501 \
  pilotforgeai:latest

# Check memory usage
docker stats pilotforge-ui
```

### Slow Performance

```bash
# Check CPU usage
docker stats --no-stream

# Increase CPU limit
docker run -d \
  --name pilotforge-ui \
  --cpus="2.0" \
  -p 8501:8501 \
  pilotforgeai:latest

# Enable GPU acceleration
docker run -d \
  --gpus all \
  --name pilotforge-gpu \
  -p 8501:8501 \
  pilotforgeai:latest
```

### Network Issues

```bash
# Test connectivity
docker exec pilotforge-ui ping google.com

# Check DNS
docker exec pilotforge-ui nslookup google.com

# Inspect network
docker network inspect bridge

# Use host network (not recommended for production)
docker run -d --network host pilotforgeai:latest
```

---

## 📚 Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **AWS ECS Guide**: https://aws.amazon.com/ecs/getting-started/
- **Azure Container Instances**: https://azure.microsoft.com/en-us/services/container-instances/
- **GCP Cloud Run**: https://cloud.google.com/run/docs
- **Kubernetes**: https://kubernetes.io/docs/home/

---

## 🆘 Support

**Issues**: [GitHub Issues](https://github.com/hneal055/EnhancedBudgetPro/issues)  
**Email**: hneal055@example.com  
**Discussions**: [GitHub Discussions](https://github.com/hneal055/EnhancedBudgetPro/discussions)

---

<p align="center">
  <strong>Last Updated</strong>: 2025-01-30<br>
  <strong>Version</strong>: 0.6.0
</p>
