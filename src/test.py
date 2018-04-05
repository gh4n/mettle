import csv
from mettle import Mettle

file = 'test.csv'

storage = Mettle()
storage.listen()

with open(file) as f:
    data = csv.DictReader(f)
    for row in data:
        key = storage.add("ticket", {"desc": row['text'], "prediction": "NULL", "actual": "NULL", "resolved": False})

        # storage.update("ticket", {key['name'] + "/prediction" : "Bad"})
        # storage.update("archive", {key['name'] + "/actual" : "Good"})
        storage.update("archive", {key['name'] + "/resolved": True})
        print()

