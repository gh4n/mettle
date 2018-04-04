import csv
from database import Mettle

file = 'test.csv'

storage = Mettle()
storage.listen()

with open(file) as f:
    data = csv.DictReader(f)
    for row in data:
        key = storage.add({"category": row['category'], "desc": row['text'], "prediction": "NULL", "actual": "NULL"})

        storage.update({key['name'] + "/prediction" : "Bad"})
        storage.update({key['name'] + "/actual" : "Good"})


