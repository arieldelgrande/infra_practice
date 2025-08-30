# ---------- Builder Stage ----------
FROM python:3.13-slim AS builder

ENV POETRY_VERSION=2.1.4
WORKDIR /app

# Install system dependencies in one layer
RUN apt-get update && \
    apt-get install -y python3-pip && \
    python3 -m pip install --upgrade pip setuptools && \
    pip install "poetry==$POETRY_VERSION" && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install poetry plugin and export dependencies
RUN poetry self add poetry-plugin-export && \
    poetry export -f requirements.txt --output requirements-test.txt --with main --with test && \
    poetry export -f requirements.txt --output requirements.txt --only main

# ---------- Common Base Stage ----------
FROM python:3.13-slim AS base

WORKDIR /app

# Copy requirements files from builder
COPY --from=builder /app/requirements.txt /app/requirements.txt
COPY --from=builder /app/requirements-test.txt /app/requirements-test.txt

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential tini && \
    rm -rf /var/lib/apt/lists/*

# ---------- Test Stage ----------
FROM base AS test

# Copy application code
COPY src/ ./src
COPY tests/ ./tests

# Set Python path
ENV PYTHONPATH=/app/src:/app

# Install test dependencies
RUN pip install --no-cache-dir -r requirements-test.txt && \
    pip install --no-cache-dir httpx pytest fastapi python-dotenv pydantic-settings

CMD ["pytest", "tests", "-v"]

# ---------- Production Stage ----------
FROM base AS prod

# Install production dependencies first
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy application code with proper ownership
COPY --chown=appuser:appgroup src/ ./src

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Use tini as the entrypoint for proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]