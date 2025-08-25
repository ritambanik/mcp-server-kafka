import csv
import json
from confluent_kafka import Producer
import os

# Confluent Cloud configuration
conf = {
    'bootstrap.servers': 'pkc-619z3.us-east1.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_API_KEY'),
    'sasl.password': os.getenv('KAFKA_API_SECRET'),
    'client.id': 'csv-producer'
}

producer = Producer(conf)


def delivery_report(err, msg):
    """Called once for each message to indicate delivery result."""
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def produce_messages(topic, filepath):
    print(f"Producing messages to topic {topic} from file {filepath}")
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            message = json.dumps(row)
            producer.produce(
                topic=topic,
                key=row.get("timestamp", None),
                value=message,
                callback=delivery_report
            )
            producer.poll(0.1)
    producer.flush()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Produce messages to Kafka from a CSV file.")
    parser.add_argument("--topic", type=str, default="ratings", help="Kafka topic to produce to", required=True)
    parser.add_argument("--file", type=str, default="src/testdatagenerator/ratings.csv", help="Path to the CSV file", required=False)
    args = parser.parse_args()
    produce_messages(args.topic, args.file)