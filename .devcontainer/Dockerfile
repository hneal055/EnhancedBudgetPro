# Optional custom Dockerfile (not used by default)
# Uncomment and modify devcontainer.json to use this instead of base image

FROM mcr.microsoft.com/devcontainers/python:3.12

# Install additional system dependencies if needed
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Pre-install common development tools
RUN pip install --upgrade pip setuptools wheel

WORKDIR /workspace
