from bson.objectid import ObjectId

class Packet:
    def __init__(self, RAW, SRC, DST, MAC, TYPE, BAIL, MASQUE, DHCP, DN, DNS, ROUTER):
        id = ObjectId()
        id_raw = ObjectId()
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
    
    def get_packet(self):
        return self.packet
    
    def get_raw(self):
        return self.raw