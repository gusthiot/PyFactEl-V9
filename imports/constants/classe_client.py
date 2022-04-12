from imports import Fichier
from core import (Outils,
                  VerifFormat,
                  ErreurConsistance)


class ClasseClient(Fichier):
    """
    Classe pour l'importation des données de Classes Clients
    """

    cles = ['id_classe', 'code_n', 'intitule', 'ref_fact', 'avantage_HC', 'subsides', 'rabais_excep', 'grille']
    nom_fichier = "classeclient.csv"
    libelle = "Classes Clients"

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_classe'], info = VerifFormat.est_un_alphanumerique(donnee['id_classe'], "l'id classe client",
                                                                          ligne)
            msg += info
            if info == "":
                if donnee['id_classe'] not in ids:
                    ids.append(donnee['id_classe'])
                else:
                    msg += "l'id classe client '" + donnee['id_classe'] + "' de la ligne " + str(ligne) + \
                           " n'est pas unique\n"

            donnee['code_n'], info = VerifFormat.est_un_alphanumerique(donnee['code_n'], "le code N", ligne)
            msg += info
            donnee['intitule'], info = VerifFormat.est_un_texte(donnee['intitule'], "l'intitulé", ligne)
            msg += info
            if donnee['ref_fact'] != 'INT' and donnee['ref_fact'] != 'EXT':
                msg += "le code référence client de la ligne " + str(ligne) + " doit être INT ou EXT\n"
            if donnee['avantage_HC'] != 'BONUS' and donnee['avantage_HC'] != 'RABAIS':
                msg += "l'avantage HC de la ligne " + str(ligne) + " doit être BONUS ou RABAIS\n"
            if donnee['subsides'] != 'BONUS' and donnee['subsides'] != 'RABAIS':
                msg += "le mode subsides de la ligne " + str(ligne) + " doit être BONUS ou RABAIS\n"
            if donnee['rabais_excep'] != 'BONUS' and donnee['rabais_excep'] != 'RABAIS':
                msg += "le mode rabais exceptionnel de la ligne " + str(ligne) + " doit être BONUS ou RABAIS\n"
            if donnee['grille'] != 'OUI' and donnee['grille'] != 'NON':
                msg += "la grille tarifaire de la ligne " + str(ligne) + " doit être OUI ou NON\n"

            donnees_dict[donnee['id_classe']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
