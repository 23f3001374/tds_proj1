FROM python:3.12-slim-bookworm

# Set working directory to /app
WORKDIR /app

# Install required tools
RUN apt-get update && apt-get install -y \
    gcc libpq-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv venv

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy application code and scripts
COPY app.py .
COPY app/ /app/  # Copy all scripts inside /app/

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
