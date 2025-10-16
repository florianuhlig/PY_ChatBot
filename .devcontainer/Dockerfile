FROM mcr.microsoft.com/devcontainers/python:1-3.8-bullseye

# Install additional tools
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    postgresql-client \
    sqlite3 \
    vim \
    curl \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install Python development tools
RUN pip install --upgrade pip \
    && pip install \
    black \
    flake8 \
    pytest \
    pytest-cov \
    ipython

# Set working directory
WORKDIR /workspace
