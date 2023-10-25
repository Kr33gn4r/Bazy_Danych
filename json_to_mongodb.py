import json, pymongo
from pymongo import MongoClient, InsertOne

client = MongoClient()
db = client.zadanie
collection = db.restaurants
requesting = []

with open(r"/home/rskay/Documents/Bazy Danych/restaurants.json", "r") as f:
    for jsonObj in f:
        dict = json.loads(jsonObj)
        requesting.append(InsertOne(dict))

result = collection.bulk_write(requesting)
client.close()