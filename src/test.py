import csv
from database import Database

file = 'test.csv'

storage = Database()
storage.listen()

with open(file) as f:
    data = csv.DictReader(f)
    for row in data:
        key = storage.add({"category": row['category'], "desc": row['text'], "prediction": "NULL", "actual": "NULL"})

        storage.update({key['name'] + "/prediction" : "Bad"})
        storage.update({key['name'] + "/actual" : "Good"})


