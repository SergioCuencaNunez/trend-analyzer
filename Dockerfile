# Use the official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variable for the port
ENV PORT 8050

# Expose the port
EXPOSE $PORT

# Specify the command to run your app using Gunicorn
CMD ["gunicorn", "-b", ":$PORT", "app_instance:server"]
