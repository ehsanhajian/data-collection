# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install PostgreSQL development files
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run kafka_consumer.py when the container launches
CMD ["python", "./kafka_consumer.py"]
