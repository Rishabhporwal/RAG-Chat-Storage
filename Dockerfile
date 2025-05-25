FROM python:3.11-slim

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev postgresql-client && apt-get clean

# Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# To make wait script executable
RUN chmod +x app/wait-for-postgres.sh

# Expose Port
EXPOSE 8000
