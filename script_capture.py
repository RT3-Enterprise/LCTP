import scapy.all as scapy # import des différentes bibliothèques (scapy,utils,request,os)
import utils
import request
import os

type_list=["","Discover","Offer","Request","Decline","Ack","Nak","Release","Inform"] # On identifie la nature de la trame grâce au numméro d'Opcode la nature depuis cette liste

def sniff_dhcp_packets(interface):  # Fonction qui permet de sniff les packets DHCP sur une interface précise (interface à définir selon le votre)
    try:    # un bloc d'essai pour gérer les exceptions
        scapy.sniff(iface=interface, store=False, prn=process_dhcp_packet, filter="udp and port 67 or port 68") # fonction sniff de scapy pour capturer les packets , iface --> interface , store --> stockage en mémoire True Or False , prn --> fonction qui sera apelle pour chaque paquet capturé, filtre udp 67 donc server DHCP et 68 client DHCP
    except KeyboardInterrupt:      # gére le Ctrl+c pour arrêter la capture de trame
        print("Arrêt de la capture.") # le script nous dis alors que la capture s'arrête

def process_dhcp_packet(packet): # Permet d'analyser ma trame dhcp pour la découpé et en resortir que les infos qui m'intérésee
    if packet.haslayer(scapy.DHCP):
        type=packet[scapy.DHCP].options[0][1]# Permet de renvoyer l'Opcode qui détermine la nature du paquet et de la stocker dans la variable "type"
        trame_type = type_list[type] # Le nom des variables ci-dessous permet de savoir ce que l'on récupére
        source_ip= packet[scapy.IP].src
        destination_ip= packet[scapy.IP].dst
        source_mac= packet[scapy.Ether].src
        destination_mac= packet[scapy.Ether].dst
        lease_time=packet[scapy.DHCP].options[2][1]
        subnet_mask=packet[scapy.DHCP].options[3][1]
        routeur=packet[scapy.DHCP].options[4][1]
        domain_name=packet[scapy.DHCP].options[5][1]
        dns_ip=packet[scapy.DHCP].options[6][1]
        dhcp_info = utils.Packet(str(packet), str(source_ip), str(destination_ip), str(source_mac), str(destination_mac), str(trame_type), str(lease_time), str(subnet_mask), str(domain_name), str(dns_ip), str(routeur)) #crée la variable dhcp_info comprenant tout les informations dhcp importante
        try:
            request.post_packet(dhcp_info)        # envoie le contenue de la variable vers la bdd
        except:
            print("Erreur lors de l'insertion du packet")

if __name__ == "__main__":    
    interface = os.getenv('INTERFACE', 'eth0')    #définition de l'interface sniffer sur l'appareil
    sniff_dhcp_packets(interface)            #lance le script pour sniffer les paquets 
