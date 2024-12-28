# Use an official Python runtime as the base image
FROM python:3.12.5-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main script and the functions directory into the container
COPY main.py .
COPY functions/ /app/functions/

# Set the entry point for the container to run the main script
ENTRYPOINT ["python", "main.py"]