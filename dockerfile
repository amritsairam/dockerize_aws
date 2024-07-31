# Use an appropriate base image
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install build dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app

# Ensure the environment variable is set for Django settings
ENV DJANGO_SETTINGS_MODULE=userauthentication.settings

# Expose the port (optional, for local testing)
EXPOSE 8000

# Run the application
CMD ["uvicorn", "userauthentication.asgi:application", "--host", "0.0.0.0", "--port", "8000"]




