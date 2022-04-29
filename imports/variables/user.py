from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class User(CsvImport):
    """
    Classe pour l'importation des données de Users
    """

    cles = ['id_user', 'sciper', 'nom', 'prenom']
    nom_fichier = "user.csv"
    libelle = "Users"

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
        # scipers = []

        for donnee in self.donnees:
            donnee['id_user'], info = Format.est_un_alphanumerique(donnee['id_user'], "l'id user", ligne)
            msg += info
            if donnee['id_user'] == "":
                msg += "l'id user de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_user'] not in ids:
                ids.append(donnee['id_user'])
            else:
                msg += "l'id user '" + donnee['id_user'] + "' de la ligne " + str(ligne) +\
                       " n'est pas unique\n"

            donnee['sciper'], info = Format.est_un_alphanumerique(donnee['sciper'], "le sciper", ligne)
            msg += info
            # if donnee['sciper'] == "":
            #     msg += "le sciper de la ligne " + str(ligne) + " ne peut être vide\n"
            # elif donnee['sciper'] not in scipers:
            #     scipers.append(donnee['sciper'])
            # else:
            #     msg += "le sciper '" + donnee['sciper'] + "' de la ligne " + str(ligne) +\
            #            " n'est pas unique\n"

            donnee['nom'], info = Format.est_un_texte(donnee['nom'], "le nom", ligne)
            msg += info
            donnee['prenom'], info = Format.est_un_texte(donnee['prenom'], "le prénom", ligne)
            msg += info

            donnees_dict[donnee['id_user']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
