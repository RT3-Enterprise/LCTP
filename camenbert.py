import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LCTPApp:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("LCTP")
        self.fenetre.geometry("600x400")
        self.fenetre.configure(bg="green")

        # Titre en rouge
        title_label = tk.Label(fenetre, text="Logiciel de capture de trame en Python", fg="red", bg='green')
        title_label.pack()

        # Menu
        menu = tk.Menu(fenetre)
        fenetre.config(menu=menu)

        # Menu Surveillance
        surveillance_menu = tk.Menu(menu)
        menu.add_cascade(label="Surveillance", menu=surveillance_menu)

        self.mac_compteur = 1
        self.ip_envoye_compteur = 1
        self.ip_disponible_compteur = 1
        self.trame_resu_compteur = 1

        surveillance_menu.add_command(label="Nombre de MAC", command=self.display_mac_compteur)
        surveillance_menu.add_command(label="Nombre d'IP envoyées", command=self.display_ip_envoye_compteur)
        surveillance_menu.add_command(label="Nombre d'IP disponibles", command=self.display_ip_disponible_compteur)
        surveillance_menu.add_command(label="Nombre de trames reçues", command=self.display_trame_resu_compteur)

        self.mac_compteur_label = tk.Label(fenetre, text=f"Nombre de MAC: {self.mac_compteur}", fg='blue', bg='green')
        self.mac_compteur_label.pack()

        self.ip_envoye_label = tk.Label(fenetre, text=f"Nombre d'IP envoyées: {self.ip_envoye_compteur}", fg='blue', bg='green')
        self.ip_envoye_label.pack()

        self.ip_disponible_label = tk.Label(fenetre, text=f"Nombre d'IP disponibles: {self.ip_disponible_compteur}", fg='blue', bg='green')
        self.ip_disponible_label.pack()

        self.trame_resu_label = tk.Label(fenetre, text=f"Nombre de trames reçues: {self.trame_resu_compteur}", fg='blue', bg='green')
        self.trame_resu_label.pack()

        # Créez un graphique camembert
        pie_chart_label = tk.Label(fenetre, text="Graphique Camembert", fg='blue', bg='green')
        pie_chart_label.pack()

        # Données pour le graphique camembert
        ip_disponibles = self.ip_disponible_compteur
        ip_envoyees = self.ip_envoye_compteur
        labels = ['IP Disponibles', 'IP Envoyées']
        sizes = [ip_disponibles, (ip_disponibles * ip_envoyees) / 100]

        # Créez le graphique camembert avec Matplotlib
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')

        # Créez un wrapper pour afficher le graphique dans Tkinter
        pie_chart_canvas = FigureCanvasTkAgg(fig, master=fenetre)
        pie_chart_canvas.get_tk_widget().pack()

        # Bouton Quitter en bas de la fenêtre
        quit_button = tk.Button(fenetre, text="Quitter", command=self.quit, bg="red", fg="yellow")
        quit_button.pack(side=tk.BOTTOM)

    def quit(self):
        self.fenetre.destroy()

    def display_mac_compteur(self):
        self.mac_compteur += 1
        self.mac_compteur_label.config(text=f"Nombre de MAC: {self.mac_compteur}")

    def display_ip_envoye_compteur(self):
        self.ip_envoye_compteur += 1
        self.ip_envoye_label.config(text=f"Nombre d'IP envoyées: {self.ip_envoye_compteur}")

    def display_ip_disponible_compteur(self):
        self.ip_disponible_compteur += 1
        self.ip_disponible_label.config(text=f"Nombre d'IP disponibles: {self.ip_disponible_compteur}")

    def display_trame_resu_compteur(self):
        self.trame_resu_compteur += 1
        self.trame_resu_label.config(text=f"Nombre de trames reçues: {self.trame_resu_compteur}")

    def display_alerte_compteur(self):
        self.alerte_compteur += 1

if __name__ == "__main__":
    fenetre = tk.Tk()
    app = LCTPApp(fenetre)
    fenetre.mainloop()
