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
        self.ip_envoye_compteur = 23
        self.ip_disponible_compteur = 50
        self.trame_resu_compteur = 1

        surveillance_menu.add_command(label="Nombre de MAC", command=self.display_mac_compteur)
        surveillance_menu.add_command(label="Nombre d'IP envoyées", command=self.display_ip_envoye_compteur)
        surveillance_menu.add_command(label="Nombre d'IP disponibles", command=self.display_ip_disponible_compteur)
        surveillance_menu.add_command(label="Nombre de trames reçues", command=self.display_trame_resu_compteur)

        self.mac_compteur_label = tk.Label(fenetre, text=f"Nombre de MAC: {self.mac_compteur}", fg='blue', bg='green')
        self.mac_compteur_label.pack()

        self.ip_envoye_label = tk.Label(fenetre, text=f"Nombre d'IP envoyées: {self.ip_envoye_compteur}", fg='blue', bg='green')
        self.ip_envoye_label.pack()

        # Entrée pour modifier ip_disponible_compteur
        self.ip_disponible_var = tk.StringVar()
        self.ip_disponible_var.set(str(self.ip_disponible_compteur))
        ip_disponible_entry_label = tk.Label(fenetre, text="Modifier IP disponibles:", fg='blue', bg='green')
        ip_disponible_entry_label.pack()
        ip_disponible_entry = tk.Entry(fenetre, textvariable=self.ip_disponible_var, fg='gray', takefocus=True, validate="all")
        ip_disponible_entry.pack()

        # Bouton pour modifier ip_disponible_compteur
        modify_button = tk.Button(fenetre, text="Modifier", command=self.modify_ip_disponible, bg="blue", fg="white")
        modify_button.pack()

        self.ip_disponible_label = tk.Label(fenetre, text=f"Nombre d'IP disponibles: {self.ip_disponible_compteur}", fg='blue', bg='green')
        self.ip_disponible_label.pack()

        self.trame_resu_label = tk.Label(fenetre, text=f"Nombre de trames reçues: {self.trame_resu_compteur}", fg='blue', bg='green')
        self.trame_resu_label.pack()

        # Créez un graphique camembert
        self.graphique_camembert_label = tk.Label(fenetre, text="Graphique Camembert", fg='blue', bg='green')
        self.graphique_camembert_label.pack()

        # Créez un wrapper pour afficher le graphique dans Tkinter
        self.graphique_camembert_canvas = None
        self.MAJ_camenbert()

        # Bouton Quitter en bas de la fenêtre
        quit_button = tk.Button(fenetre, text="Quitter", command=self.quit, bg="red", fg="yellow")
        quit_button.pack(side=tk.BOTTOM)

        # Bouton Alerte
        alerte_button = tk.Button(fenetre, text="Alerte", command=self.create_alert_window, bg="red", fg="white")
        alerte_button.pack(side=tk.RIGHT)

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

    def MAJ_camenbert(self):
        if self.graphique_camembert_canvas:
            self.graphique_camembert_canvas.get_tk_widget().destroy()

        # Données pour le graphique camembert
        ip_disponibles = self.ip_disponible_compteur
        ip_envoyees = self.ip_envoye_compteur
        labels = ["IP disponibles", "IP envoyées"]
        sizes = [ip_disponibles-ip_envoyees, ip_envoyees]
        colors = ['yellowgreen', 'red']
        # crée le graphique camembert
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        # Créez un wrapper pour afficher le graphique dans Tkinter
        self.graphique_camembert_canvas = FigureCanvasTkAgg(fig, master=self.fenetre)
        self.graphique_camembert_canvas.get_tk_widget().pack()

        # Mettre à jour le camembert toutes les 1 seconde
        self.fenetre.after(1000, self.MAJ_camenbert)

    def modify_ip_disponible(self):
        new_value = int(self.ip_disponible_var.get())
        self.ip_disponible_compteur = new_value
        self.ip_disponible_label.config(text=f"Nombre d'IP disponibles: {self.ip_disponible_compteur}")

    def create_alert_window(self):
        alert_window = tk.Toplevel(self.fenetre)
        alert_window.title("Alerte")
        alert_window.geometry("400x300")
        alert_window.configure(bg="red")

        # Liste d'erreurs fictives
        errors = ["Erreur 1: Description de l'erreur 1",
                  "Erreur 2: Description de l'erreur 2",
                  "Erreur 3: Description de l'erreur 3"]

        # Afficher la liste d'erreurs dans la nouvelle fenêtre
        for page_error in errors:
            page_error_label = tk.Label(alert_window, text=page_error, fg='white', bg='red')
            page_error_label.pack()

if __name__ == "__main__":
    fenetre = tk.Tk()
    app = LCTPApp(fenetre)
    app.MAJ_camenbert()  # Appel initial pour commencer la boucle de mise à jour du camembert
    fenetre.mainloop()
