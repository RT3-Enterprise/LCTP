# Import des noms du module
from tkinter import *
# Création d'un objet "fenêtre"
fenetre = Tk()
# Titre (Label)
fenetre.title("LCTP")
fenetre.minsize(770,380)
titre = Label(fenetre, text = "Logiciel de Capture de Trame en Python")
titre.configure(fg = 'red')
# Affichage du titre
titre.pack()
# Ajout des autres widgets
cadre = Frame(fenetre)
cadre.pack()
'''test(fenetre, test)'''
bouton = Button(cadre, text = "test",)
bouton.pack()
'''
messagebox.showwarning("Message d'avertissement", "Ceci est un message d'avertissement")
messagebox.showinfo("Message info", "Ceci est un message d'information")'''
# .........................
bouton_quitter = Button(cadre, text = "Quitter", command = fenetre.quit)
bouton_quitter.pack()
# Démarrage de la boucle Tkinter (à placer à la fin !!!)
fenetre.mainloop()