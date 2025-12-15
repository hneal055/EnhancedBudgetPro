# PILOTFORGEAI Production Dockerfile
# Multi-stage build for optimized image size

# Stage 1: Base image with Python
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies
FROM base as dependencies

WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Application
FROM dependencies as application

# Copy application code
COPY . .

# Create output directories
RUN mkdir -p output batch_output web_output

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Set working directory
WORKDIR /app

# Default command: Run Streamlit UI
CMD ["streamlit", "run", "ui_app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
