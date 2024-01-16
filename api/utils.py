from bson.objectid import ObjectId
from bson import json_util
import json

class Packet:
    def __init__(self, RAW, SRC, DST, MAC, TYPE, BAIL, MASQUE, DHCP, DN, DNS, ROUTER):
        id = str(ObjectId())
        id_raw = str(ObjectId())
        self.raw = {
            "_id": id_raw,
            "RAW": RAW
        }
        self.packet = {
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
        