FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy pyproject and lock files
COPY backend/pyproject.toml backend/poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --only main

# Copy application code
COPY backend/. .

# Expose port
EXPOSE 8000

# Command to run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
