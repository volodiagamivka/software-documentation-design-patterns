import csv

class DataProcessor:
    def __init__(self, strategy):
        self._strategy = strategy

    def run(self, file_path, limit=10):
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                # Очищуємо назви колонок від можливих лапок або пробілів
                reader.fieldnames = [name.strip('"').strip() for name in reader.fieldnames]
                
                data_to_send = []
                for _ in range(limit):
                    try:
                        data_to_send.append(next(reader))
                    except StopIteration:
                        break
                
                self._strategy.send(data_to_send)
        except Exception as e:
            print(f"Error reading CSV: {e}")