import pymongo
import os
import utils
import json

DB_URL = os.getenv('DATABASE_URL', 'mongo_bdd') # URL de la BDD (default: localhost)
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

def json_to_packet(json_data):
    data = json.loads(json_data)
    data_raw = data[0]
    data_packet = data[1]
    data = utils.Packet(data_raw['RAW'], data_packet['SRC'], data_packet['DST'], data_packet['MAC_SRC'], data_packet['MAC_DST'], data_packet['TYPE'], data_packet['BAIL'], data_packet['MASQUE'], data_packet['DN'], data_packet['DNS'], data_packet['ROUTER'], data_packet['_id'], data_raw['_id'])
    return data

def initiate_LCTP(client1=None):
    if client1 is None:
        client1 = client()
    db = client1["LCTP"]
    raw = db["raw"]
    trames = db["trames"]
    return raw, trames

def insert_packet(client, packet:utils.Packet):
    raw, trames = initiate_LCTP(client)
    insert_json(raw, packet.raw)
    insert_json(trames, packet.packet)

def delete_packet(client, packet:utils.Packet):
    raw, trames = initiate_LCTP(client)
    delete_json(raw, packet.raw)
    delete_json(trames, packet.packet)
    
def change_packet(client, packet:utils.Packet, new_packet:utils.Packet):
    raw, trames = initiate_LCTP(client)
    change_json(raw, packet.raw, new_packet.raw)
    change_json(trames, packet.packet, new_packet.packet)
    
def get_db(client):
    raw, trames = initiate_LCTP(client)
    RAW = []
    TRAMES = []
    for e in raw.find():
        RAW.append(e)
    for e in trames.find():
        TRAMES.append(e)
    return RAW, TRAMES

def initiate_Baux(client1=None):
    if client1 is None:
        client1 = client()
    db = client1["LCTP"]
    baux = db["baux"]
    return baux

def get_baux(client):
    baux = initiate_Baux(client)
    BAUX = []
    for e in baux.find():
        BAUX.append(e)
    return BAUX

def insert_baux(client, baux:utils.Baux):
    baux = initiate_Baux(client)
    insert_json(baux, baux.baux)
    
def delete_baux(client, baux:utils.Baux):
    baux = initiate_Baux(client)
    delete_json(baux, baux.baux)
    
def change_baux(client, baux:utils.Baux, new_baux:utils.Baux):
    baux = initiate_Baux(client)
    change_json(baux, baux.baux, new_baux.baux)
    
def json_to_baux(json_data):
    data = json.loads(json_data)
    data = utils.Baux(data['IP'], data['BAIL'], data['_id'])
    return data

def get_baux_by_id(client, id):
    baux = initiate_Baux(client)
    return get_json_by_id(baux, id)