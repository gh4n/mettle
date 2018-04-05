import csv
import time
from mettle import Mettle

file = 'test.csv'

storage = Mettle()
storage.listen()

with open(file) as f:
    data = csv.DictReader(f)
    for row in data:
        print(row)
        key = storage.add("tickets", {"desc": row['text'], "prediction": "NULL", "confidence":"NULL", "actual": "NULL", "resolved": False})
        # storage.update("ticket", {key['name'] + "/prediction" : "Bad"})
        # storage.update("archive", {key['name'] + "/actual" : "Good"})
        # storage.update("tickets", {key['name'] + "/resolved": True})



        # TICKETS SHOULD BE EMPTY, ARCHIVE SHOULD BE FULL