from kafka import KafkaConsumer
import psycopg2
import os

# Kafka Consumer
consumer = KafkaConsumer(
    'temperature-data',
    bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVERS']],
    auto_offset_reset='earliest'
)

# PostgreSQL Connection
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    database=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD']
)
cur = conn.cursor()

for message in consumer:
    data = message.value.decode('utf-8')
    parts = data.split(': ')
    if len(parts) == 2:
        city = parts[0]
        temperature = float(parts[1].replace('°C', ''))

        # Insert into TimescaleDB
        cur.execute(
            "INSERT INTO temperature_data (time, city, temperature) VALUES (NOW(), %s, %s);",
            (city, temperature)
        )
        conn.commit()
    else:
        print(f"Unexpected data format: {data}")

cur.close()
conn.close()
