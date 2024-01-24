import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QSizePolicy, QTextEdit, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import request

default = request.get_trame_first()

# Configuration réseau par défaut
IP_DHCP_DEFAULT = default.source_ip if 
MASK_DEFAULT = default.subnet_mask
MAC_DHCP_DEFAULT = default.source_mac
GATEWAY_DEFAULT = default.routeur
ip_disponibles = 50
ip_envoyees = 24
nombre_MAC = 1
nombre_trames_recues = 1

#Valeurs obtenues de l'API (à remplacer par la logique de récupération des valeurs de l'API de nicolas)
IP_DHCP_TRAM = "192.168.1.2"
MASK_TRAM = "255.255.255.5"
MAC_DHCP_TRAM = "AA:BB:CC:DD:EE:FF"
GATEWAY_TRAM = "192.168.1.254"

#b
class LCTPApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Configuration de la fenêtre principale
        self.setWindowTitle("LCTP")
        self.setGeometry(100, 100, 600, 400)  
        self.setStyleSheet("background-color: lightgreen")  

        # Initialisation des fenêtres de paramètres et d'alertes
        self.param_fenetre = None
        self.alert_fenetre = None
        self.trames_fenetre = None
        
        # Configuration de la disposition des widgets dans la fenêtre principale
        # Création d'un widget central pour la fenêtre principale
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Création d'un layout principal en utilisant QVBoxLayout pour le widget central
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Configuration des marges du layout principal

        # Création d'un layout horizontal pour le haut de la fenêtre principale
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)  # Ajout du layout horizontal au layout principal

        # Création d'un layout vertical pour les paramètres à gauche dans le layout horizontal
        param_layout = QVBoxLayout()
        top_layout.addLayout(param_layout)  # Ajout du layout des paramètres au layout horizontal
        param_layout.setContentsMargins(0, 0, 10, 0)  # Configuration des marges du layout des paramètres

        # Création d'un layout vertical pour les informations réseau à droite dans le layout horizontal
        info_reseaux_layout = QVBoxLayout()
        top_layout.addLayout(info_reseaux_layout)  # Ajout du layout des informations réseau au layout horizontal

        # Création d'un layout vertical pour le graphique en bas de la fenêtre principale
        graphique_layout = QVBoxLayout()
        main_layout.addLayout(graphique_layout)  # Ajout du layout du graphique au layout principal

        # Création d'un layout horizontal pour les boutons en bas de la fenêtre principale
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)  # Ajout du layout des boutons au layout principal

        # Widgets pour les informations du réseau (champs de texte)
        self.ip_dhcp_line_edit = QLineEdit(IP_DHCP_DEFAULT)  # Champ de texte pour l'IP du serveur DHCP, valeur par défaut
        self.mask_line_edit = QLineEdit(MASK_DEFAULT)  # Champ de texte pour le masque de sous-réseaux, valeur par défaut
        self.mac_dhcp_line_edit = QLineEdit(MAC_DHCP_DEFAULT)  # Champ de texte pour l'adresse MAC du serveur DHCP, valeur par défaut
        self.gateway_line_edit = QLineEdit(GATEWAY_DEFAULT)  # Champ de texte pour l'adresse de la passerelle, valeur par défaut

        # Ajout des widgets dans les layouts correspondants
        param_layout.addWidget(QLabel("IP du serveur DHCP:"))  # Ajoute un label "IP du serveur DHCP" au layout
        param_layout.addWidget(self.ip_dhcp_line_edit)  # Ajoute le champ de texte correspondant à l'IP du serveur DHCP au layout
        param_layout.addWidget(QLabel("Masque de sous-réseaux:"))  # Ajoute un label "Masque de sous-réseaux" au layout
        param_layout.addWidget(self.mask_line_edit)  # Ajoute le champ de texte correspondant au masque de sous-réseaux au layout
        param_layout.addWidget(QLabel("Adresse MAC du serveur DHCP:"))  # Ajoute un label "Adresse MAC du serveur DHCP" au layout
        param_layout.addWidget(self.mac_dhcp_line_edit)  # Ajoute le champ de texte correspondant à l'adresse MAC du serveur DHCP au layout
        param_layout.addWidget(QLabel("Adresse de la passerelle:"))  # Ajoute un label "Adresse de la passerelle" au layout
        param_layout.addWidget(self.gateway_line_edit)  # Ajoute le champ de texte correspondant à l'adresse de la passerelle au layout

        # Labels pour les informations du réseau (avec valeurs par défaut)
        self.ip_dhcp_label = QLabel(f"IP du serveur DHCP: {IP_DHCP_DEFAULT}")  # Label pour l'IP du serveur DHCP avec sa valeur par défaut
        self.mask_label = QLabel(f"Masque de sous-réseaux: {MASK_DEFAULT}")  # Label pour le masque de sous-réseaux avec sa valeur par défaut
        self.mac_dhcp_label = QLabel(f"Adresse MAC du serveur DHCP: {MAC_DHCP_DEFAULT}")  # Label pour l'adresse MAC du serveur DHCP avec sa valeur par défaut
        self.gateway_label = QLabel(f"Adresse de la passerelle: {GATEWAY_DEFAULT}")  # Label pour l'adresse de la passerelle avec sa valeur par défaut
        self.ip_disponible_label = QLabel(f"Nombre d'IP disponibles: {ip_disponibles}")  # Label pour le nombre d'IP disponibles avec sa valeur
        self.mac_compteur_label = QLabel(f"Nombre de MAC: {nombre_MAC}")  # Label pour le nombre de MAC avec sa valeur
        self.ip_envoye_label = QLabel(f"Nombre d'IP envoyées: {ip_envoyees}")  # Label pour le nombre d'IP envoyées avec sa valeur
        self.trame_resu_label = QLabel(f"Nombre de trames reçues: {nombre_trames_recues}")  # Label pour le nombre de trames reçues avec sa valeur

        # Ajout des labels dans les layouts correspondants
        info_reseaux_layout.addWidget(self.ip_disponible_label)
        info_reseaux_layout.addWidget(self.mac_compteur_label)
        info_reseaux_layout.addWidget(self.ip_envoye_label)
        info_reseaux_layout.addWidget(self.trame_resu_label)

        # Widget pour afficher le graphique camembert
        self.graphique_widget = QWidget()
        graphique_layout.addWidget(self.graphique_widget)
        self.cree_camembert()

#a 
        # Boutons pour Paramètres, Alerte et Quitter
        # Création du bouton "Quitter"
        quit_button = QPushButton("Quitter", self)
        quit_button.setStyleSheet("background-color: red; color: white")  # Définition du style du bouton
        quit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Configuration de la politique de taille du bouton
        quit_button.clicked.connect(self.close)  # Connexion du signal clicked à la méthode close de la fenêtre principale

        # Création du bouton "Paramètres"
        param_button = QPushButton("Paramètres", self)
        param_button.setStyleSheet("background-color: blue; color: white")  # Définition du style du bouton
        param_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Configuration de la politique de taille du bouton
        param_button.clicked.connect(self.ouvrir_param_fenetre)  # Connexion du signal clicked à la méthode ouvrir_param_fenetre de la fenêtre principale

        # Création du bouton "Alerte"
        alerte_button = QPushButton("Alerte", self)
        alerte_button.setStyleSheet("background-color: red; color: white")  # Définition du style du bouton
        alerte_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Configuration de la politique de taille du bouton
        alerte_button.clicked.connect(self.ouvrir_alert_fenetre)  # Connexion du signal clicked à la méthode ouvrir_alert_fenetre de la fenêtre principale

        # Ajout des boutons dans le layout dédié aux boutons
        button_layout.addWidget(param_button)  # Ajout du bouton Paramètres dans le layout des boutons
        button_layout.addWidget(alerte_button)  # Ajout du bouton Alerte dans le layout des boutons
        button_layout.addWidget(quit_button)  # Ajout du bouton Quitter dans le layout des boutons
        
        #testg
        trames_button = QPushButton("Trames", self)
        trames_button.setStyleSheet("background-color: yellow; color: black")
        trames_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        trames_button.clicked.connect(self.ouvrir_trames_fenetre)
        button_layout.addWidget(trames_button)

    def cree_camembert(self):
        # Fonction pour créer et afficher le graphique camembert
        labels = ["IP disponibles", "IP envoyées"]  # Libellés pour les sections du camembert
        sizes = [ip_disponibles - ip_envoyees, ip_envoyees]  # Tailles des sections
        colors = ['yellowgreen', 'red']  # Couleurs correspondantes

        fig, ax = plt.subplots()  # Création d'une figure et d'axes pour le camembert
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)  # Création du camembert
        ax.axis('equal')  # Ajustement de l'axe pour un camembert circulaire

        canvas = FigureCanvas(fig)  # Utilisation d'un canevas pour afficher la figure
        layout = QVBoxLayout(self.graphique_widget)  # Layout pour le widget graphique
        layout.addWidget(canvas)  # Ajout du canevas dans le layout

    def ouvrir_param_fenetre(self):
        # Fonction pour ouvrir la fenêtre des paramètres
        if self.param_fenetre and self.param_fenetre.isVisible():
            self.param_fenetre.close()  # Fermeture de la fenêtre si elle est déjà ouverte
        self.param_fenetre = ParamWindow(self)  # Création de la fenêtre Paramètres
        self.param_fenetre.show()  # Affichage de la fenêtre des paramètres

    def ouvrir_alert_fenetre(self):
        # Fonction pour ouvrir la fenêtre d'alerte
        if self.alert_fenetre and self.alert_fenetre.isVisible():
            self.alert_fenetre.close()  # Fermeture de la fenêtre si elle est déjà ouverte (évite le beug de superposition des fenêtres)
        self.alert_fenetre = AlertWindow(self)  # Création de la fenêtre Alerte
        self.alert_fenetre.show()  # Affichage de la fenêtre d'alerte
        
#test3
    def ouvrir_trames_fenetre(self):
        if self.trames_fenetre and self.trames_fenetre.isVisible():
            self.trames_fenetre.close()
        self.trames_fenetre = TramesWindow(self)
        self.trames_fenetre.show()

#c
class ParamWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # Appel du constructeur de la classe parente (QWidget)
        self.setWindowTitle("Paramètres")  # Définition du titre de la fenêtre
        self.setGeometry(200, 200, 400, 300)  # Position et taille de la fenêtre
        self.setStyleSheet("background-color: #383838; color: white")  # Style de la fenêtre

        layout = QVBoxLayout(self)  # Création d'un layout vertical pour organiser les widgets

        # Création des champs de texte pour les paramètres par défaut
        self.ip_dhcp_line_edit = QLineEdit(IP_DHCP_DEFAULT)
        self.mask_line_edit = QLineEdit(MASK_DEFAULT)
        self.mac_dhcp_line_edit = QLineEdit(MAC_DHCP_DEFAULT)
        self.gateway_line_edit = QLineEdit(GATEWAY_DEFAULT)

        # Ajout des labels et des champs de texte dans le layout
        layout.addWidget(QLabel("IP du serveur DHCP:", self))
        layout.addWidget(self.ip_dhcp_line_edit)
        layout.addWidget(QLabel("Masque de sous-réseaux:", self))
        layout.addWidget(self.mask_line_edit)
        layout.addWidget(QLabel("Adresse MAC du serveur DHCP:", self))
        layout.addWidget(self.mac_dhcp_line_edit)
        layout.addWidget(QLabel("Adresse de la passerelle:", self))
        layout.addWidget(self.gateway_line_edit)

        # Création d'un bouton "Appliquer" pour valider les changements
        apply_button = QPushButton("Appliquer", self)
        apply_button.clicked.connect(self.apply_changes)  # Connexion du signal clicked à la méthode apply_changes
        layout.addWidget(apply_button)  # Ajout du bouton dans le layout

        # Création d'un bouton "Fermer" pour fermer la fenêtre
        ferme_button = QPushButton("Fermer", self)
        ferme_button.clicked.connect(self.close)  # Connexion du signal clicked à la méthode close
        layout.addWidget(ferme_button)  # Ajout du bouton dans le layout

    def apply_changes(self):
        # Méthode pour appliquer les changements aux champs de texte dans la fenêtre principale
        parent_window = self.parent()  # Récupération de la fenêtre principale
        # Mise à jour des champs de texte dans la fenêtre principale avec les nouvelles valeurs
        parent_window.ip_dhcp_line_edit.setText(self.ip_dhcp_line_edit.text())
        parent_window.mask_line_edit.setText(self.mask_line_edit.text())
        parent_window.mac_dhcp_line_edit.setText(self.mac_dhcp_line_edit.text())
        parent_window.gateway_line_edit.setText(self.gateway_line_edit.text())
        self.close()  # Fermeture de la fenêtre de paramètres après application des changements

#e
# Définition d'une nouvelle fenêtre pour afficher les alertes
class AlertWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # Appel du constructeur de la classe parente (QWidget)
        self.setWindowTitle("Alerte")  # Définition du titre de la fenêtre
        self.setGeometry(200, 200, 540, 300)  # Position et taille de la fenêtre
        self.setStyleSheet("background-color: red; color: white")  # Style de la fenêtre

        layout = QVBoxLayout(self)  # Création d'un layout vertical pour organiser les widgets
        # Logique de comparaison des valeurs par défaut avec celles de l'API
        errors = []  # Initialisation d'une liste pour stocker les erreurs détectées
        if IP_DHCP_TRAM != IP_DHCP_DEFAULT:  # Vérification si l'IP DHCP de la tram est différente de celle par défaut
            errors.append(f"ERREUR IP_DHCP_TRAM différente de IP_DHCP_DEFAULT: {IP_DHCP_TRAM} != {IP_DHCP_DEFAULT}")
        if MASK_TRAM != MASK_DEFAULT:  # Vérification si le masque de la tram est différent de celui par défaut
            errors.append(f"ERREUR MASK_TRAM différent de MASK_DEFAULT: {MASK_TRAM} != {MASK_DEFAULT}")
        if MAC_DHCP_TRAM != MAC_DHCP_DEFAULT:  # Vérification si l'adresse MAC DHCP de la tram est différente de celle par défaut
            errors.append(f"ERREUR MAC_DHCP_TRAM différent de MAC_DHCP_DEFAULT: {MAC_DHCP_TRAM} != {MAC_DHCP_DEFAULT}")
        if GATEWAY_TRAM != GATEWAY_DEFAULT:  # Vérification si la passerelle de la tram est différente de celle par défaut
            errors.append(f"ERREUR GATEWAY_TRAM différent de GATEWAY_DEFAULT: {GATEWAY_TRAM} != {GATEWAY_DEFAULT}")
        # Ajout d'une vérification si le nombre d'IP envoyées est supérieur au nombre d'IP disponibles
        if ip_envoyees > ip_disponibles:
            errors.append(f"ERREUR: Plus d'IP disponibles - IP envoyées ({ip_envoyees}) > IP disponibles ({ip_disponibles})")

#f
        if not errors:  # Vérification s'il n'y a pas d'erreur détectée
            errors.append("Il n'y a pas d'erreur détectée.")  # Message par défaut s'il n'y a pas d'erreur

        # Ajout des messages d'erreur dans des labels à la fenêtre
        for error in errors:
            label = QLabel(error, self)  # Création d'un label pour chaque message d'erreur
            layout.addWidget(label)  # Ajout du label dans le layout vertical

        ferme_button = QPushButton("Fermer", self)  # Création d'un bouton pour fermer la fenêtre
        ferme_button.clicked.connect(self.close)  # Connexion du signal clicked à la méthode close
        layout.addWidget(ferme_button)  # Ajout du bouton dans le layout

#testg
# Définition d'une nouvelle fenêtre pour afficher les trames capturées
class TramesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Trames Capturées")  # Définition du titre de la fenêtre
        self.setGeometry(200, 200, 600, 400)  # Définition de la position et de la taille de la fenêtre
        self.setStyleSheet("background-color: white")  # Définition du style de fond de la fenêtre

        # Ajout d'une section pour afficher les trames capturées
        self.trames_edit = QTextEdit(self)  # Création d'un widget QTextEdit pour afficher les trames
        self.trames_edit.setReadOnly(True)  # Configuration du mode lecture seule pour le champ de texte des trames

        # Ajout d'une section pour entrer le filtre
        self.filtre_edit = QTextEdit(self)  # Création d'un widget QTextEdit pour entrer le filtre

        # Ajout d'un bouton pour appliquer le filtre et obtenir les trames
        apply_button = QPushButton("Appliquer Filtre", self)  # Création d'un bouton avec le texte "Appliquer Filtre"
        apply_button.clicked.connect(self.appliquer_filtre)  # Connexion du signal clicked à la méthode appliquer_filtre

        # Créez un layout vertical pour organiser les widgets
        layout = QVBoxLayout(self)  # Création d'un layout vertical pour la fenêtre
        layout.addWidget(QLabel("Filtre:", self))  # Ajout d'un label "Filtre:" à la fenêtre
        layout.addWidget(self.filtre_edit)  # Ajout du champ de texte du filtre dans le layout
        layout.addWidget(apply_button)  # Ajout du bouton "Appliquer Filtre" dans le layout
        layout.addWidget(QLabel("Trames Capturées:", self))  # Ajout d'un label "Trames Capturées:" à la fenêtre
        layout.addWidget(self.trames_edit)  # Ajout du champ de texte des trames dans le layout

    def appliquer_filtre(self):
        # Méthode pour appliquer le filtre et obtenir les trames
        filtre = self.filtre_edit.toPlainText()  # Récupération du texte du champ de texte du filtre
        # Voir avec l'API (fonction non définie ici)
        trames = obtenir_trames_avec_filtre(filtre)  # Appel de la fonction pour obtenir les trames avec le filtre
        self.trames_edit.setPlainText(trames)  # Affichage des trames dans le champ de texte des trames

#i
if __name__ == "__main__": # Vérification si le fichier est exécuté directement
    app = QApplication(sys.argv) # Création de l'application
    mainWin = LCTPApp() # Création de la fenêtre principale
    mainWin.show() # Affichage de la fenêtre principale
    sys.exit(app.exec_()) 
    #fin