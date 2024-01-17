import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Configuration réseau par défaut
IP_DHCP_DEFAULT = "192.168.1.1"
MASK_DEFAULT = "255.255.255.0"
MAC_DHCP_DEFAULT = "AA:BB:CC:DD:EE:FF"
GATEWAY_DEFAULT = "192.168.1.254"
ip_disponibles = 50
ip_envoyees = 23
nombre_MAC = 1
nombre_trames_recues = 1

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

        # Configuration de la disposition des widgets dans la fenêtre principale
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        param_layout = QVBoxLayout()
        top_layout.addLayout(param_layout)
        param_layout.setContentsMargins(0, 0, 10, 0)

        info_reseaux_layout = QVBoxLayout()
        top_layout.addLayout(info_reseaux_layout)

        graphique_layout = QVBoxLayout()
        main_layout.addLayout(graphique_layout)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        # Widgets pour les informations du réseau (labels et champs de texte)
        self.ip_dhcp_line_edit = QLineEdit(IP_DHCP_DEFAULT)
        self.mask_line_edit = QLineEdit(MASK_DEFAULT)
        self.mac_dhcp_line_edit = QLineEdit(MAC_DHCP_DEFAULT)
        self.gateway_line_edit = QLineEdit(GATEWAY_DEFAULT)

        # Ajout des widgets dans les layouts correspondants
        param_layout.addWidget(QLabel("IP du serveur DHCP:"))
        param_layout.addWidget(self.ip_dhcp_line_edit)
        param_layout.addWidget(QLabel("Masque de sous-réseaux:"))
        param_layout.addWidget(self.mask_line_edit)
        param_layout.addWidget(QLabel("Adresse MAC du serveur DHCP:"))
        param_layout.addWidget(self.mac_dhcp_line_edit)
        param_layout.addWidget(QLabel("Adresse de la passerelle:"))
        param_layout.addWidget(self.gateway_line_edit)

        # Labels pour les informations du réseau
        self.ip_dhcp_label = QLabel(f"IP du serveur DHCP: {IP_DHCP_DEFAULT}")
        self.mask_label = QLabel(f"Masque de sous-réseaux: {MASK_DEFAULT}")
        self.mac_dhcp_label = QLabel(f"Adresse MAC du serveur DHCP: {MAC_DHCP_DEFAULT}")
        self.gateway_label = QLabel(f"Adresse de la passerelle: {GATEWAY_DEFAULT}")

        self.ip_disponible_label = QLabel(f"Nombre d'IP disponibles: {ip_disponibles}")
        self.mac_compteur_label = QLabel(f"Nombre de MAC: {nombre_MAC}")
        self.ip_envoye_label = QLabel(f"Nombre d'IP envoyées: {ip_envoyees}")
        self.trame_resu_label = QLabel(f"Nombre de trames reçues: {nombre_trames_recues}")

        # Ajout des labels dans les layouts correspondants
        info_reseaux_layout.addWidget(self.ip_disponible_label)
        info_reseaux_layout.addWidget(self.mac_compteur_label)
        info_reseaux_layout.addWidget(self.ip_envoye_label)
        info_reseaux_layout.addWidget(self.trame_resu_label)

        # Widget pour afficher le graphique camembert
        self.graphique_widget = QWidget()
        graphique_layout.addWidget(self.graphique_widget)
        self.create_pie_chart()

        # Boutons pour Paramètres, Alerte et Quitter
        quit_button = QPushButton("Quitter", self)
        quit_button.setStyleSheet("background-color: red; color: white")
        quit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        quit_button.clicked.connect(self.close)

        param_button = QPushButton("Paramètres", self)
        param_button.setStyleSheet("background-color: blue; color: white")
        param_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        param_button.clicked.connect(self.ouvrir_param_fenetre)

        alerte_button = QPushButton("Alerte", self)
        alerte_button.setStyleSheet("background-color: red; color: white")
        alerte_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        alerte_button.clicked.connect(self.ouvrir_alert_fenetre)

        # Ajout des boutons dans le layout dédié aux boutons
        button_layout.addWidget(param_button)
        button_layout.addWidget(alerte_button)
        button_layout.addWidget(quit_button)

    def create_pie_chart(self):
        # Fonction pour créer et afficher le graphique camembert
        labels = ["IP disponibles", "IP envoyées"]
        sizes = [ip_disponibles - ip_envoyees, ip_envoyees]
        colors = ['yellowgreen', 'red']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        canvas = FigureCanvas(fig)
        layout = QVBoxLayout(self.graphique_widget)
        layout.addWidget(canvas)

    def ouvrir_param_fenetre(self):
        # Fonction pour ouvrir la fenêtre des paramètres
        if self.param_fenetre and self.param_fenetre.isVisible():
            self.param_fenetre.close()
        self.param_fenetre = ParamWindow(self)
        self.param_fenetre.show()

    def ouvrir_alert_fenetre(self):
        # Fonction pour ouvrir la fenêtre d'alerte
        if self.alert_fenetre and self.alert_fenetre.isVisible():
            self.alert_fenetre.close()
        self.alert_fenetre = AlertWindow(self)
        self.alert_fenetre.show()

class ParamWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: #383838; color: white")

        layout = QVBoxLayout(self)


        self.ip_dhcp_line_edit = QLineEdit(IP_DHCP_DEFAULT)
        self.mask_line_edit = QLineEdit(MASK_DEFAULT)
        self.mac_dhcp_line_edit = QLineEdit(MAC_DHCP_DEFAULT)
        self.gateway_line_edit = QLineEdit(GATEWAY_DEFAULT)

        layout.addWidget(QLabel("IP du serveur DHCP:", self))
        layout.addWidget(self.ip_dhcp_line_edit)
        layout.addWidget(QLabel("Masque de sous-réseaux:", self))
        layout.addWidget(self.mask_line_edit)
        layout.addWidget(QLabel("Adresse MAC du serveur DHCP:", self))
        layout.addWidget(self.mac_dhcp_line_edit)
        layout.addWidget(QLabel("Adresse de la passerelle:", self))
        layout.addWidget(self.gateway_line_edit)

        apply_button = QPushButton("Appliquer", self)
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        ferme_button = QPushButton("Fermer", self)
        ferme_button.clicked.connect(self.close)
        layout.addWidget(ferme_button)

    def apply_changes(self):
        parent_window = self.parent()
        parent_window.ip_dhcp_line_edit.setText(self.ip_dhcp_line_edit.text())
        parent_window.mask_line_edit.setText(self.mask_line_edit.text())
        parent_window.mac_dhcp_line_edit.setText(self.mac_dhcp_line_edit.text())
        parent_window.gateway_line_edit.setText(self.gateway_line_edit.text())
        self.close()


class AlertWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Alerte")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: red; color: white")

        layout = QVBoxLayout(self)

        errors = ["Erreur 1: Description de l'erreur 1",
                  "Erreur 2: Description de l'erreur 2",
                  "Erreur 3: Description de l'erreur 3"]

        for error in errors:
            label = QLabel(error, self)
            layout.addWidget(label)

        ferme_button = QPushButton("Fermer", self)
        ferme_button.clicked.connect(self.close)
        layout.addWidget(ferme_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = LCTPApp()
    mainWin.show()
    sys.exit(app.exec_())