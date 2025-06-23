FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install uv (must be in a RUN)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add pyproject files early for caching
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies globally
RUN uv sync --system

# Create a non-root user and switch
RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app
USER myuser

# Copy your app code
COPY agent_manage/ ./agent_manage/
COPY main.py .

# Set environment
ENV PATH="/home/myuser/.local/bin:$PATH"

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
