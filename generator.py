import csv
import random
import os

def generate_unique_data(filename="data/data.csv", count=1050):
    if not os.path.exists('data'):
        os.makedirs('data')

    headers = ['userID', 'email', 'gameID', 'title', 'status', 'price', 'progress']
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for i in range(1, count + 1):
            user_id = f"user_unique_{i}"
            game_id = 40000 + i  
            
            writer.writerow({
                'userID': user_id,
                'email': f"player_{i}@steam.ua",
                'gameID': game_id,
                'title': f"Game Vol.{i}",
                'status': random.choice(['Installed', 'Running', 'In Library']),
                'price': random.choice([0.0, 19.99, 29.50, 59.99, 9.99]),
                'progress': f"{random.randint(0, 100)}%"
            })
            

if __name__ == "__main__":
    generate_unique_data()