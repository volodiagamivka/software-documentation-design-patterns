import json
from bll.processor import DataProcessor
from strategies.console_strategy import ConsoleOutput
from strategies.redis_strategy import RedisOutput
from strategies.kafka_strategy import KafkaOutput

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def get_strategy(config):
    mode = config.get("output_mode", "console").lower()
    if mode == "redis":
        return RedisOutput()
    elif mode == "kafka":
        return KafkaOutput()
    return ConsoleOutput()

if __name__ == "__main__":
    cfg = load_config()
    strategy = get_strategy(cfg)
    processor = DataProcessor(strategy)
    processor.run("data/nypd_data.csv", limit=10)