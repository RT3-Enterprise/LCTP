import scapy.all as scapy # import de la bibliothèque scapy
type_list=["","Discover","Offer","Request","Decline","Ack","Nak","Release","Inform"] # On identifie grâce au numméro d'Opcode la nature depuis cette liste
def sniff_dhcp_packets(interface):  # definition de la fonction sniff_dhcp_packets d'argument interface, il capture les packets dhcp
    try:    # un bloc d'essai pour gérer les exceptions
        scapy.sniff(iface=interface, store=False, prn=process_dhcp_packet, filter="udp and port 67 or port 68") # fonction sniff de scapy pour capturer les packets , iface --> interface , store --> stockage en mémoire True Or False , prn --> fonction qui sera apelle pour chaque paquet capturé, filtre udp 67 donc server DHCP et 68 client DHCP
    except KeyboardInterrupt:      # gére le Ctrl+c pour arrêter la capture de trame
        print("Arrêt de la capture.") # le script nous dis alors que la capture s'arrête

def process_dhcp_packet(packet): # definition de la fonction process_dhcp_packet d'argument packet
    if packet.haslayer(scapy.DHCP): # haslayer permet de vérifier ci le packet capturé est bien un packet DHCP de type ACK grace à  "== 5"
        type=packet[scapy.DHCP].options[0][1]# Permet de renvoyer l'Opcode qui détermine la nature du paquet et de la stocker dans la variable "type"
        trame_type = type_list[type]
        Source_IP= packet[scapy.IP].src
        Destination_IP= packet[scapy.IP].dst
        Source_MAC= packet[scapy.Ether].src
        Destination_MAC= packet[scapy.Ether].dst
        Lease_Time=packet[scapy.DHCP].options[2][1]
        Subnet_Mask=packet[scapy.DHCP].options[3][1]
        Routeur=packet[scapy.DHCP].options[4][1]
        Domain_Name=packet[scapy.DHCP].options[5][1]
        DNS_Ip= packet[scapy.DHCP].options[6][1]
        return trame_type,Source_IP,Destination_IP,Source_MAC,Destination_MAC,Lease_Time,Subnet_Mask,Routeur,DNS_Ip






if __name__ == "__main__":
    interface = "eth0"  # Remplacez par le nom de votre interface réseau (par exemple, "eth0")
    sniff_dhcp_packets(interface)

