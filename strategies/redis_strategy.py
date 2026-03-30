import redis
import json
from core.interfaces import IOutputStrategy

class RedisOutput(IOutputStrategy):
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def send(self, data: list):
        for i, record in enumerate(data):
            self.client.set(f"death_stat:{i}", json.dumps(record))
        print(f"Successfully sent {len(data)} records to Redis")