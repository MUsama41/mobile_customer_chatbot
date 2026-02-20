FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv for dependency management
RUN pip install --no-cache-dir uv

# Copy dependency metadata first (better Docker layer caching)
COPY pyproject.toml uv.lock ./

# Use uv+uv.lock to install dependencies into the global environment (no venv)
RUN uv export --no-dev --output-file requirements.txt \
    && uv pip install --system --requirement requirements.txt

# Copy application code
COPY . .

# Expose API port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
