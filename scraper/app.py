#!/usr/bin/env python3
import time
import requests
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def fetch_temperature(producer):
    cities = ["Zurich", "London", "Miami", "Tokyo", "Singapore"]
    for city in cities:
        response = requests.get(f"https://wttr.in/{city}?format=%t")
        temperature = response.text.strip()
        data = f"Temperature in {city}: {temperature}"
        producer.produce('temperature-data', data.encode('utf-8'), callback=delivery_report)
        producer.flush()

if __name__ == "__main__":
    producer = Producer({'bootstrap.servers': 'my-kafka-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092'})
    while True:
        fetch_temperature(producer)
        time.sleep(300)  # Sleep for 300 seconds (5 minutes)
