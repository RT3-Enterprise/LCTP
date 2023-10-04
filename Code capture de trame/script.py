import scapy.all as scapy # import de la bibliothèque scapy

def sniff_dhcp_packets(interface):  # definition de la fonction sniff_dhcp_packets d'argument interface, il capture les packets dhcp
    try:    # un bloc d'essai pour gérer les exceptions
        scapy.sniff(iface=interface, store=False, prn=process_dhcp_packet, filter="udp and port 67 or port 68") # fonction sniff de scapy pour capturer les packets , iface --> interface , store --> stockage en mémoire True Or False , prn --> fonction qui sera apelle pour chaque paquet capturé, filtre udp 67 donc server DHCP et 68 client DHCP
    except KeyboardInterrupt:      # gére le Ctrl+c pour arrêter la capture de trame
        print("Arrêt de la capture.") # le script nous dis alors que la capture s'arrête

def process_dhcp_packet(packet): # definition de la fonction process_dhcp_packet d'argument packet
    if packet.haslayer(scapy.DHCP) and packet[scapy.DHCP].options[0][1] == 5: # haslayer permet de vérifier ci le packet capturé est bien un packet DHCP de type ACK grace à  "== 5"
        print("----- Trame DHCP Capturée -----") # permet de différencier les trames en marquant le début du packet
        print(f"Source IP: {packet[scapy.IP].src}, Destination IP: {packet[scapy.IP].dst}") #
        print(f"Source MAC: {packet[scapy.Ether].src}, Destination MAC: {packet[scapy.Ether].dst}")
        print("Lease Time: ", packet[scapy.DHCP].options[2][1])
        print("Subnet Mask: ", packet[scapy.DHCP].options[3][1])
        print("Server IP: ", packet[scapy.DHCP].options[4][1])
        print("DNS IP: ", packet[scapy.DHCP].options[5][1])
        print("Domain Name: ", packet[scapy.DHCP].options[6][1])
        print("---------------------------------") #permet de marquer la fin du packet
if __name__ == "__main__":
    interface = "eth0"  # Remplacez par le nom de votre interface réseau (par exemple, "eth0")
    sniff_dhcp_packets(interface)
