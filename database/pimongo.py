import pymongo
from json.objectid import ObjectId

DB_URL = "localhost"
DB_PORT = 27017

def startup_db_client():
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
    result = collection.find_one({"_id": ObjectId(id)})
    if result is None:
        raise Exception("Failed to get json data by id")
    return result

def get_packet(RAW, SRC, DST, MAC, TYPE, BAIL, MASQUE, DHCP, DN, DNS, ROUTER):
    id = ObjectId()
    id_raw = ObjectId()
    raw = {
        "_id": id_raw,
        "RAW": RAW
    }
    packet = {
        "_id": id,
        "RAW_ID": id_raw,
        "SRC": SRC,
        "DST": DST,
        "MAC": MAC,
        "TYPE": TYPE,
        "BAIL": BAIL,
        "MASQUE": MASQUE,
        "DHCP": DHCP,
        "DN": DN,
        "DNS": DNS,
        "ROUTER": ROUTER
    }
    return raw, packet

def initiate_LCTP():
    client = startup_db_client()
    db = client["LCTP"]
    raw = db["raw"]
    trames = db["trames"]
    return raw, trames

def insert_packet():
    raw, trames = initiate_LCTP()
    data = ilker()
    packet = get_packet(data)
    insert_json(raw, packet[0])
    insert_json(trames, packet[1])
    
def get_db():
    raw, trames = initiate_LCTP()
    RAW = []
    TRAMES = []
    for e in raw.find():
        RAW.append(e)
    for e in trames.find():
        TRAMES.append(e)
    return RAW, TRAMES
    
    
