from kafka import KafkaProducer
import json
from core.interfaces import IOutputStrategy

class KafkaOutput(IOutputStrategy):
    def __init__(self, bootstrap_servers='localhost:9092'):
        # Створюємо реального продюсера
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send(self, data: list):
        print("=== KAFKA REAL OUTPUT ===")
        for record in data:
            # Відправляємо кожен рядок у топік 'nyc_mortality'
            self.producer.send('nyc_mortality', value=record)
        
        # Чекаємо завершення відправки всіх повідомлень
        self.producer.flush()
        print(f"Successfully sent {len(data)} messages to Kafka.")