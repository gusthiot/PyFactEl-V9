from tkinter.filedialog import askdirectory
from tkinter.scrolledtext import ScrolledText
from tkinter import *

import platform
import sys
import os

from core import ErreurConsistance


class Interface(object):
    """
    Classe contenant diverses méthodes liées à l'interface utilisateur
    """

    if platform.system() in ['Linux', 'Darwin']:
        _interface_graphique = len(os.environ.get('DISPLAY', '')) > 0
    else:
        _interface_graphique = True

    @classmethod
    def interface_graphique(cls, opt_nouvelle_valeur=None):
        """
        enregistre que l'on veut l'interface graphique ou non
        :param opt_nouvelle_valeur: True ou False pour interface graphique
        :return: valeur enregistrée
        """
        if opt_nouvelle_valeur is not None:
            cls._interface_graphique = opt_nouvelle_valeur
        return cls._interface_graphique

    @classmethod
    def affiche_message(cls, message):
        """
        affiche une petite boite de dialogue avec un message et un bouton OK
        :param message: message à afficher
        """
        if cls.interface_graphique():
            fenetre = Tk()
            fenetre.title("Message")
            texte = ScrolledText(fenetre)
            texte.insert(END, message)
            texte.pack()
            button = Button(fenetre, text='OK', command=fenetre.destroy)
            button.pack()
            mainloop()
        else:
            print(message)

    @classmethod
    def fatal(cls, exn, message):
        """
        affiche erreur fatal
        :param exn: erreur
        :param message: message à afficher
        """
        Interface.affiche_message(message + "\n" + str(exn))
        if isinstance(exn, ErreurConsistance) or isinstance(exn, ValueError):
            sys.exit(1)
        else:
            sys.exit(4)

    @classmethod
    def affiche_message_conditionnel(cls, titre, message):
        """
        affiche une petite boite de dialogue avec un message et 2 boutons OUI/NON, le NON arrête le programme
        :param titre: titre à afficher
        :param message: message à afficher
        """
        if cls.interface_graphique():
            fenetre = Tk()
            fenetre.title(titre)
            texte = ScrolledText(fenetre)
            texte.insert(END, message)
            texte.pack()
            button = Button(fenetre, text='OUI', command=fenetre.destroy)
            button.pack(side="left")
            button = Button(fenetre, text='NON', command=sys.exit)
            button.pack(side="right")
            mainloop()
        else:
            sys.exit("message conditionnel non-autorisé en mode sans graphique")

    @staticmethod
    def choisir_dossier():
        """
        affiche une interface permettant de choisir un dossier
        :return: la position du dossier sélectionné
        """
        fenetre = Tk()
        fenetre.title("Choix du dossier")
        dossier = askdirectory(parent=fenetre, initialdir="/",
                               title='Choisissez un dossier de travail')
        fenetre.destroy()
        if dossier == "":
            Interface.affiche_message("Aucun dossier choisi")
            sys.exit("Aucun dossier choisi")
        return dossier + "/"
