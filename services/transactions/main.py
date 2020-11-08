import json
from kafka import KafkaConsumer

KAFKA_BROKER_URL = "kafka:9092"
TRANSACTIONS_TOPIC = "payments"


if __name__ == '__main__':
    consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
    )
    for message in consumer:
        transaction: dict = message.value
        print("TRANSACTION SUCCEEDED")
        print(transaction)
