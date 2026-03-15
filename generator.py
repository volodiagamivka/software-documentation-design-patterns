import csv
import random
import os

def generate():
    if not os.path.exists('data'): os.makedirs('data')
    with open('data/data.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['userID', 'email', 'gameID', 'title', 'status', 'price', 'progress'])
        writer.writeheader()
        for i in range(1001):
            writer.writerow({
                'userID': f'u{random.randint(1, 100)}',
                'email': f'user{i}@test.com',
                'gameID': random.randint(100, 500),
                'title': f'SteamGame_{i}',
                'status': 'Active',
                'price': random.choice([0, 19.99, 49.99]),
                'progress': f'{random.randint(1, 100)}%'
            })
    print("📁 Файл data/data.csv створено (1000+ рядків).")

if __name__ == "__main__":
    generate()