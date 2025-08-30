# ---------- Builder Stage ----------
FROM python:3.13.3-slim AS builder

ENV POETRY_VERSION=2.1.3

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Copy dependency files
COPY poetry.lock pyproject.toml ./

# Install poetry plugin and export dependencies
RUN poetry self add poetry-plugin-export && \
    poetry export -f requirements.txt --output requirements.txt --only main && \
    poetry export -f requirements.txt --output requirements-test.txt --with test

# ---------- Common Base Stage ----------
FROM python:3.13.3-slim AS base

# make Python output unbuffered (good for logs)
ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Install tini, a lightweight init system for containers that reaps zombie processes
RUN apt-get update && \
    apt-get install -y --no-install-recommends tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user and group for security
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

# Create and set permissions for the virtual environment
RUN python -m venv $VIRTUAL_ENV
RUN chown -R appuser:appgroup /opt/venv

WORKDIR /app
RUN chown -R appuser:appgroup /app
USER appuser

WORKDIR /app

# ---------- Test Stage ----------
FROM base AS test

# Copy application code
USER root
COPY --from=builder /app/requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt
COPY --chown=appuser:appgroup src/ ./src
COPY --chown=appuser:appgroup tests/ ./tests
USER appuser
CMD ["pytest"]

# ---------- Production Stage ----------
FROM base AS prod
# in pipeline delete these when impemented
ENV ENV=production
COPY --from=builder /app/requirements.txt .

# Install production dependencies into the virtual environment
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appgroup src/ ./src
EXPOSE 8080

# Use tini as the entrypoint to handle signals and reap zombie processes
ENTRYPOINT ["/usr/bin/tini", "--"]

# Run the application with Gunicorn for better performance and process management
CMD [ "gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "-b", "0.0.0.0:8080"]