FROM python:3.11-slim

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose Port
EXPOSE 8000

# Run the app
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
