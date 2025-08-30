# ---------- Builder Stage ----------
FROM python:3.13-slim as builder

ENV POETRY_VERSION=2.1.3
WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock* ./

# Install poetry export plugin
RUN poetry self add poetry-plugin-export

# Export production dependencies
RUN poetry export -f requirements.txt --output requirements.txt --only main

# Export dev dependencies (including main) for testing
RUN poetry export -f requirements.txt --output requirements-test.txt --with test

# ---------- Common Base Stage ----------
FROM python:3.13-slim as base

WORKDIR /app

# Copy requirements files from builder
COPY --from=builder /app/requirements.txt /app/requirements.txt
COPY --from=builder /app/requirements-test.txt /app/requirements-test.txt

# Install build essentials for some dependencies (optional, remove if not needed)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# ---------- Test Stage ----------
FROM base as test

COPY src/ ./src
COPY .env ./
COPY tests/ ./tests

RUN pip install --no-cache-dir -r requirements-test.txt

# Example test command (adjust as needed)
CMD ["pytest", "tests"]

# ---------- Production Stage ----------
FROM base as prod

COPY src/ ./src
COPY .env ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]