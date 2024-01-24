import requests
import os
import json
import utils

API_URL = os.getenv('API_URL', 'http://localhost:5000/api/v1/resources/')


def get(url): # Fonction pour faire des requêtes GET
    return requests.get(url).json()

def get_packet_all(): # Fonction pour récupérer tous les packets
    return get(API_URL + '/packet/all')

def get_raw_all(): # Fonction pour récupérer tous les raw
    return get(API_URL + '/raw/all')

def get_trame_flitered(filter, only=False): # Fonction pour récupérer les trames filtrées
    if only:
        filter['only'] = 'True'
    return requests.get(API_URL + '/trame', params=filter).json()

def get_trame_all(): # Fonction pour récupérer toutes les trames
    return get(API_URL + '/trame/all')

def post_packet(packet:utils.Packet): # Fonction pour poster un packet
    json_packet = packet.to_json_all()
    return requests.post(API_URL + '/packet', json=json_packet)

def delete_packet(packet:utils.Packet): # Fonction pour supprimer un packet
    json_packet = packet.to_json_all()
    return requests.delete(API_URL + '/packet', json=json_packet)

def put_packet(packet:utils.Packet, new_packet:utils.Packet): # Fonction pour modifier un packet
    json_packet = packet.to_json_all()
    json_new_packet = new_packet.to_json_all()
    data = {
        'json': json_packet,
        'json_new': json_new_packet
    }
    return requests.put(API_URL + '/packet', json=data)

def get_baux_all(): # Fonction pour récupérer tous les baux
    return get(API_URL + '/baux/all')

def get_baux_filtered(filter): # Fonction pour récupérer les baux filtrés
    return requests.get(API_URL + '/baux', params=filter).json()

def ip_in_baux(ip): # Fonction pour vérifier si une ip est dans les baux
    return get_baux_filtered({'IP': ip}) if len(get_baux_filtered({'IP': ip})) > 0 else False

def post_baux(baux:utils.Baux): # Fonction pour poster un baux
    json_baux = baux.to_json()
    return requests.post(API_URL + '/baux', json=json_baux)

def put_baux(baux:utils.Baux, new_baux:utils.Baux): # Fonction pour modifier un baux
    # A FAIRE
    json_baux = baux.to_json()
    json_new_baux = new_baux.to_json()
    data = {
        'json': json_baux,
        'json_new': json_new_baux
    }
    return requests.put(API_URL + '/baux', json=data)

def put_baux_ip(ip): # Fonction pour modifier un baux en fonction de son ip
    # A FAIRE
    content = ip_in_baux(ip)
    if content:
        bail = json_to_baux(content)
        
    else:
        return post_baux(bail)

def delete_baux(baux:utils.Baux): # Fonction pour supprimer un baux
    json_baux = baux.to_json()
    return requests.delete(API_URL + '/baux', json=json_baux)

# Tests