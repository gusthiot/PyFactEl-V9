import shutil
import os

from core import (Chemin, Interface)


class Outils(object):
    """
    Classe contenant diverses méthodes utiles
    """

    @staticmethod
    def format_heure(nombre):
        """
        transforme une heure d'un format float à un format hh:mm
        :param nombre: heure en float
        :return: heure en hh:mm
        """
        if nombre == 0:
            return "00:00"
        signe = ""
        if nombre < 0:
            signe = "-"
        nombre = abs(nombre)
        heures = "%d" % (nombre // 60)
        if (nombre // 60) < 10:
            heures = '0' + heures
        minutes = "%d" % (nombre % 60)
        if (nombre % 60) < 10:
            minutes = '0' + minutes
        return signe + heures + ':' + minutes

    @staticmethod
    def renommer_dossier(ancienne_structure, nouvelle_structure):
        """
        renomme un dossier
        :param ancienne_structure: éléments de l'ancien nom de dossier
        :param nouvelle_structure: éléments du nouveau nom de dossier
        """
        ancien_chemin = ""
        for element in ancienne_structure:
            ancien_chemin += str(element) + Chemin.separateur_os()
        nouveau_chemin = ""
        for element in nouvelle_structure:
            nouveau_chemin += str(element) + Chemin.separateur_os()
        os.rename(ancien_chemin, nouveau_chemin)

    @staticmethod
    def effacer_fichier(chemin):
        """
        efface un fichier
        :param chemin: chemin du fichier
        """
        titre = "Effacer un fichier"
        message = "Voulez-vous vraiment effacer le fichier ? : " + chemin
        Interface.affiche_message_conditionnel(titre, message)
        os.remove(chemin)

    @staticmethod
    def effacer_dossier(chemin):
        """
        efface un dossier
        :param chemin: chemin du dossier
        """
        titre = "Effacer un dossier et son contenu"
        message = "Voulez-vous vraiment effacer le dossier (et son contenu) ? : " + chemin
        Interface.affiche_message_conditionnel(titre, message)
        shutil.rmtree(chemin)

    @staticmethod
    def lien_dossier(structure, facturation):
        """
        construit le chemin pour enregistrer les données sans vérifier son existence
        :param structure: éléments du chemin
        :param facturation: paramètres de facturation
        :return:chemin logique complet pour dossier
        """
        chemin = ""
        for element in structure:
            chemin += str(element) + Chemin.separateur_os()
        return Chemin.eliminer_double_separateur(Chemin.separateur_lien(chemin, facturation))

