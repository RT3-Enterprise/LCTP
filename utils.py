from bson.objectid import ObjectId
from bson import json_util
import json

class Packet:
    def __init__(self, RAW, SRC, DST, MAC_SRC, MAC_DST, TYPE, BAIL, MASQUE, DN, DNS, ROUTER, id=None, id_raw=None):
        id = str(ObjectId()) if id == None else id
        id_raw = str(ObjectId()) if id_raw == None else id_raw
        self.raw = {
            "_id": id_raw,
            "RAW": RAW
        }
        self.packet = {
            "_id": id,
            "RAW_ID": id_raw,
            "SRC": SRC,
            "DST": DST,
            "MAC_SRC": MAC_SRC,
            "MAC_DST": MAC_DST,
            "TYPE": TYPE,
            "BAIL": BAIL,
            "MASQUE": MASQUE,
            "DN": DN,
            "DNS": DNS,
            "ROUTER": ROUTER
        }
        
    def to_json(self):
        return json_util.dumps(self.packet)
    
    def to_json_raw(self):
        return json_util.dumps(self.raw)
    
    def to_json_all(self):
        return json_util.dumps([self.raw, self.packet])
    
class Baux:
    def __init__(self, IP, BAIL, id=None):
        id = str(ObjectId()) if id == None else id
        self.baux = {
            "_id": id,
            "IP": IP,
            "BAIL": BAIL
        }
    
    def to_json(self):
        return json_util.dumps(self.baux)