import json

DATABASE_FILE = 'database.json'


with open(DATABASE_FILE, 'r') as f:
    data = json.load(f)
    for key, value in data.items():
        print(key)