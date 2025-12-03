# Dockerfile

# Stage 1: Build Stage (Includes tools to compile dependencies like psycopg2)
FROM python:3.11-slim as builder

# Install necessary system dependencies for building Python packages (like psycopg2)
# and cleaning up afterwards to keep the image small
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy requirements and install
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image (Slim and production-ready)
# Use a clean, smaller base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy installed packages from the builder stage
# This ensures that 'celery' is available in the final image's PATH
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the entire application code
COPY . /code/

# Create necessary directories for file logging and ensure appropriate permissions
RUN mkdir -p /logs_storage && chmod -R 777 /logs_storage

# The CMD is defined in docker-compose.yml for the specific service
