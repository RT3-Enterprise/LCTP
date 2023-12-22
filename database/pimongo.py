import pymongo
import os
import utils

DB_URL = os.getenv('DATABASE_URL', 'localhost') # URL de la BDD (default: localhost)
DB_PORT = os.getenv('DATABASE_PORT', 27017) # Port de la BDD (default: 27017)

def client():
    mongodb_client = pymongo.MongoClient(DB_URL, DB_PORT)
    if mongodb_client is None:
        raise Exception("Failed to connect to MongoDB")
    return mongodb_client

def insert_json(collection, json_data):
    result = collection.insert_one(json_data)
    if result is None:
        raise Exception("Failed to insert json data")
    return result

def change_json(collection, json_data, new_json_data):
    result = collection.update_one(json_data, new_json_data)
    if result is None:
        raise Exception("Failed to change json data")
    return result

def delete_json(collection, json_data):
    result = collection.delete_one(json_data)
    if result is None:
        raise Exception("Failed to delete json data")
    return result

def get_json_by_id(collection, id):
    result = collection.find_one({"_id": pymongo.ObjectId(id)})
    if result is None:
        raise Exception("Failed to get json data by id")
    return result

def initiate_LCTP():
    client = client()
    db = client["LCTP"]
    raw = db["raw"]
    trames = db["trames"]
    return raw, trames

def insert_packet(packet:utils.Packet):
    raw, trames = initiate_LCTP()
    insert_json(raw, packet.get_packet)
    insert_json(trames, packet.get_raw)
    
def get_db():
    raw, trames = initiate_LCTP()
    RAW = []
    TRAMES = []
    for e in raw.find():
        RAW.append(e)
    for e in trames.find():
        TRAMES.append(e)
    return RAW, TRAMES