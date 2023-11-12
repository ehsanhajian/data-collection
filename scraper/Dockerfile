# Use the official Python image
FROM python:3.8

# Install Python requests and confluent-kafka libraries
RUN pip install requests confluent-kafka

# Copy the scraper script into the container
COPY app.py .

# Command to run the script
CMD ["python", "app.py"]
