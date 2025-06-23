FROM python:3.13-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Create non-root user
RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app

# Copy application code
COPY --chown=myuser:myuser agent_manager/ ./agent_manager/
COPY --chown=myuser:myuser main.py .

USER myuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]