import csv
from core.interfaces import ICSVDataSource

class CsvLoader(ICSVDataSource): 
    def get_data(self, path):
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                
                return list(csv.DictReader(f))
        except FileNotFoundError:
            print(f"error file {path} not found")
            return []