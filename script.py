import scapy.all as scapy # import de la bibliothèque scapy
import utils
import db
type_list=["","Discover","Offer","Request","Decline","Ack","Nak","Release","Inform"] # On identifie grâce au numméro d'Opcode la nature depuis cette liste
client = db.client()
class DhcpPacketInfo: #initialisation de l'object 
    def __init__(self, trame_type, source_ip, destination_ip, source_mac, destination_mac, lease_time, subnet_mask, routeur, domain_name, dns_ip):
        self.trame_type = trame_type
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.source_mac = source_mac
        self.destination_mac = destination_ip
        self.lease_time = lease_time
        self.subnet_mask = subnet_mask
        self.routeur = routeur
        self.domain_name = domain_name
        self.dns_ip = dns_ip

def sniff_dhcp_packets(interface):  # definition de la fonction sniff_dhcp_packets d'argument interface, il capture les packets dhcp
    try:    # un bloc d'essai pour gérer les exceptions
        scapy.sniff(iface=interface, store=False, prn=process_dhcp_packet, filter="udp and port 67 or port 68") # fonction sniff de scapy pour capturer les packets , iface --> interface , store --> stockage en mémoire True Or False , prn --> fonction qui sera apelle pour chaque paquet capturé, filtre udp 67 donc server DHCP et 68 client DHCP
    except KeyboardInterrupt:      # gére le Ctrl+c pour arrêter la capture de trame
        print("Arrêt de la capture.") # le script nous dis alors que la capture s'arrête

def process_dhcp_packet(packet): # definition de la fonction process_dhcp_packet d'argument packet
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
        dhcp_info = utils.Packet(packet, source_ip, destination_ip, source_mac, destination_mac, trame_type, lease_time, subnet_mask, domain_name, dns_ip, routeur)
        try:
            db.insert_packet(client, dhcp_info)
        except:
            print("Erreur lors de l'insertion du packet")

if __name__ == "__main__":
    interface = "eth0"  # Remplacez par le nom de votre interface réseau (par exemple, "eth0")
    sniff_dhcp_packets(interface)

