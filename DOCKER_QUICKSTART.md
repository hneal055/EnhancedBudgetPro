# 🐳 Docker Quick Start Guide

## What We Built

Your PILOTFORGEAI project now has complete Docker containerization with:

### 1. Dockerfile (Multi-Stage Optimized)
- **Stage 1 (Builder)**: Compiles dependencies with gcc/g++
- **Stage 2 (Runtime)**: Minimal image with only runtime requirements
- **Size**: ~800MB (300MB compressed)
- **Base**: python:3.12-slim

### 2. docker-compose.yml (Multi-Service)
- **Streamlit UI**: Port 8501
- **Flask Web App**: Port 5000
- **Shared volumes** for output and samples
- **Health checks** for both services
- **Auto-restart** policies

---

## Quick Start Commands

### Build the Image
```bash
# From project root
docker build -t pilotforgeai:latest .

# Build with progress
docker build --progress=plain -t pilotforgeai:latest .

# Check image size
docker images pilotforgeai
```

### Run Single Container

#### Option 1: Streamlit UI (Recommended)
```bash
docker run -d \
  --name pilotforge-ui \
  -p 8501:8501 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/samples:/app/samples:ro \
  --restart unless-stopped \
  pilotforgeai:latest

# Access at http://localhost:8501
```

#### Option 2: Flask Web App
```bash
docker run -d \
  --name pilotforge-web \
  -p 5000:5000 \
  -v $(pwd)/web_output:/app/web_output \
  -v $(pwd)/samples:/app/samples:ro \
  --restart unless-stopped \
  pilotforgeai:latest python web_app.py

# Access at http://localhost:5000
```

#### Option 3: GPU Support
```bash
docker run -d \
  --gpus all \
  --name pilotforge-gpu \
  -p 8501:8501 \
  -v $(pwd)/output:/app/output \
  pilotforgeai:latest

# Check GPU detection
docker logs pilotforge-gpu | grep -i cuda
```

### Run Multi-Service (docker-compose)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f streamlit
docker-compose logs -f web

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

## Container Management

### View Running Containers
```bash
docker ps
docker ps -a  # Show all (including stopped)
```

### View Logs
```bash
# Real-time logs
docker logs -f pilotforge-ui

# Last 100 lines
docker logs --tail 100 pilotforge-ui

# Logs since 1 hour ago
docker logs --since 1h pilotforge-ui
```

### Execute Commands Inside Container
```bash
# Open bash shell
docker exec -it pilotforge-ui bash

# Run Python command
docker exec pilotforge-ui python -c "print('Hello from container!')"

# Check installed packages
docker exec pilotforge-ui pip list
```

### Monitor Resources
```bash
# Real-time stats
docker stats

# Stats for specific container
docker stats pilotforge-ui

# One-time stats
docker stats --no-stream
```

### Stop and Remove
```bash
# Stop container
docker stop pilotforge-ui

# Remove container
docker rm pilotforge-ui

# Force remove (stop + remove)
docker rm -f pilotforge-ui

# Remove all stopped containers
docker container prune
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check container status
docker ps -a | grep pilotforge

# View detailed logs
docker logs pilotforge-ui

# Inspect container configuration
docker inspect pilotforge-ui

# Check if port is already in use
lsof -i :8501  # Linux/Mac
netstat -ano | findstr :8501  # Windows
```

**Common Issues**:
1. **Port already in use**: Change port mapping `-p 8502:8501`
2. **Volume permission denied**: Add `--user $(id -u):$(id -g)`
3. **Out of memory**: Increase Docker memory in Docker Desktop settings

### Build Fails

```bash
# Clean build (no cache)
docker build --no-cache -t pilotforgeai:latest .

# Check disk space
docker system df

# Clean unused images
docker image prune

# Full cleanup (careful!)
docker system prune -a
```

### GPU Not Detected

```bash
# Check NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi

# Install NVIDIA Container Toolkit (Ubuntu/Debian)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

---

## Environment Variables

### Streamlit Configuration
```bash
docker run -d \
  -e STREAMLIT_SERVER_PORT=8080 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  -e STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
  -e STREAMLIT_THEME_BASE=dark \
  -p 8080:8080 \
  pilotforgeai:latest
```

### Python Configuration
```bash
docker run -d \
  -e PYTHONUNBUFFERED=1 \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -e TORCH_HOME=/app/.cache/torch \
  pilotforgeai:latest
```

---

## Volume Mounts

### Persistent Data
```bash
docker run -d \
  -v $(pwd)/output:/app/output \           # Analysis output
  -v $(pwd)/web_output:/app/web_output \   # Web uploads
  -v $(pwd)/samples:/app/samples:ro \      # Sample scripts (read-only)
  -v $(pwd)/custom:/app/custom \           # Custom directory
  pilotforgeai:latest
```

### Windows Paths
```bash
# Use forward slashes or escape backslashes
docker run -d -v C:/Users/You/output:/app/output pilotforgeai:latest
```

---

## Health Checks

### Manual Health Check
```bash
# Streamlit health endpoint
curl http://localhost:8501/_stcore/health

# Expected response: "ok"
```

### Auto Health Check (Built into Dockerfile)
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501/_stcore/health')" || exit 1
```

### Check Health Status
```bash
docker inspect --format='{{.State.Health.Status}}' pilotforge-ui
# Returns: healthy | unhealthy | starting
```

---

## Docker Compose Services

### Service Architecture
```yaml
services:
  streamlit:
    ports: [8501:8501]
    volumes: [output, samples]
    command: streamlit run ui_app.py
    
  web:
    ports: [5000:5000]
    volumes: [web_output, samples]
    command: python web_app.py
```

### Service Commands
```bash
# Start specific service
docker-compose up -d streamlit

# Restart service
docker-compose restart streamlit

# View service logs
docker-compose logs -f streamlit

# Scale service (multiple instances)
docker-compose up -d --scale streamlit=3
```

---

## Production Deployment

### Tag and Push to Docker Hub
```bash
# Login to Docker Hub
docker login

# Tag image
docker tag pilotforgeai:latest yourusername/pilotforgeai:0.6.0
docker tag pilotforgeai:latest yourusername/pilotforgeai:latest

# Push
docker push yourusername/pilotforgeai:0.6.0
docker push yourusername/pilotforgeai:latest
```

### Pull and Run
```bash
# Anyone can now run
docker pull yourusername/pilotforgeai:latest
docker run -p 8501:8501 yourusername/pilotforgeai:latest
```

### Resource Limits
```bash
# Limit CPU and memory
docker run -d \
  --name pilotforge-limited \
  --cpus="2.0" \
  --memory="4g" \
  --memory-swap="4g" \
  -p 8501:8501 \
  pilotforgeai:latest
```

---

## Testing the Build

### Quick Test Script
```bash
#!/bin/bash
set -e

echo "🔨 Building Docker image..."
docker build -t pilotforgeai:test .

echo "🚀 Starting container..."
docker run -d --name test-container -p 8501:8501 pilotforgeai:test

echo "⏳ Waiting for service to start..."
sleep 10

echo "🔍 Testing health endpoint..."
curl -f http://localhost:8501/_stcore/health || exit 1

echo "✅ Container is healthy!"

echo "🛑 Stopping test container..."
docker stop test-container
docker rm test-container

echo "🎉 Docker build test passed!"
```

---

## Next Steps

1. **Build locally**:
   ```bash
   cd /workspaces/EnhancedBudgetPro
   docker build -t pilotforgeai:latest .
   ```

2. **Test single service**:
   ```bash
   docker run -p 8501:8501 pilotforgeai:latest
   # Open http://localhost:8501
   ```

3. **Test multi-service**:
   ```bash
   docker-compose up -d
   # Open http://localhost:8501 (Streamlit)
   # Open http://localhost:5000 (Flask)
   ```

4. **Deploy to cloud**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for AWS/Azure/GCP

---

## Docker Files Overview

```
.
├── Dockerfile              # Multi-stage build definition
├── docker-compose.yml      # Multi-service orchestration
├── .dockerignore          # Build optimization
└── .github/workflows/
    └── ci-cd.yml          # Automated Docker builds
```

---

## Useful Links

- **Docker Documentation**: https://docs.docker.com/
- **Docker Hub**: https://hub.docker.com/
- **Multi-stage Builds**: https://docs.docker.com/build/building/multi-stage/
- **Docker Compose**: https://docs.docker.com/compose/

---

**Ready to containerize!** 🐳

Run `docker build -t pilotforgeai:latest .` to get started.
