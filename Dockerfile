# Use the official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required to build h5py
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    pkg-config \
    python3-h5py

# Copy the requirements file from the src directory into the container
COPY src/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory into the container
COPY src /app

# Set environment variable for the port
ENV PORT 8080

# Expose the port
EXPOSE $PORT

# Specify the command to run your app using Gunicorn
CMD ["gunicorn", "-b", ":8080", "app:server"]
