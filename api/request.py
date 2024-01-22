import requests
import os
import json
import utils

API_URL = os.getenv('API_URL', 'http://localhost:5000/api/v1/resources/')


def get(url):
    return requests.get(url).json()

def get_packet_all():
    return get(API_URL + '/packet/all')

def get_raw_all():
    return get(API_URL + '/raw/all')

def get_trame_flitered(filter, only=False):
    if only:
        filter['only'] = 'True'
    return requests.get(API_URL + '/trame', params=filter).json()

def get_trame_all():
    return get(API_URL + '/trame/all')

def post_packet(packet:utils.Packet):
    json_packet = packet.to_json_all()
    return requests.post(API_URL + '/packet', json=json_packet)

def delete_packet(packet:utils.Packet):
    json_packet = packet.to_json_all()
    return requests.delete(API_URL + '/packet', json=json_packet)

def put_packet(packet:utils.Packet, new_packet:utils.Packet):
    json_packet = packet.to_json_all()
    json_new_packet = new_packet.to_json_all()
    data = {
        'json': json_packet,
        'json_new': json_new_packet
    }
    return requests.put(API_URL + '/packet', json=data)

p = utils.Packet('RAW1', 'SRC1', 'DST1', 'MAC1', 'TYPE1', 'BAIL1', 'MASQUE1', 'DHCP1', 'DN1', 'DNS1', 'ROUTER1')
post_packet(p)

params = {'SRC':'SRC1'}
result = get_trame_flitered(params)
print(json.dumps(result, indent=4, sort_keys=True))

delete_packet(p)
print(json.dumps(get_packet_all(), indent=4, sort_keys=True))