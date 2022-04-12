from imports import Fichier
from core import (Outils,
                  VerifFormat,
                  ErreurConsistance)


class Plateforme(Fichier):
    """
    Classe pour l'importation des données de Plateformes
    """

    nom_fichier = "plateforme.csv"
    cles = ['id_plateforme', 'code_p', 'centre', 'fonds', 'abrev_plat', 'int_plat', 'grille']
    libelle = "Plateformes"

    def __init__(self, dossier_source, clients, edition, chemin_grille):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param clients: clients importés
        :param edition: paramètres d'édition
        :param chemin_grille: dossier devant contenir la grille tarifaire
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 1
        donnees_dict = {}
        abrevs = []
        ids = []

        del self.donnees[0]
        for donnee in self.donnees:
            if donnee['id_plateforme'] == "":
                msg += "l'id plateforme " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_plateforme'] not in clients.donnees.keys():
                msg += "l'id plateforme de la ligne " + str(ligne) + " n'existe pas dans les clients \n"
            elif donnee['id_plateforme'] not in ids:
                ids.append(donnee['id_plateforme'])
            else:
                msg += "l'id plateforme de la ligne " + str(ligne) + " n'est pas unique \n"

            donnee['code_p'], info = VerifFormat.est_un_alphanumerique(donnee['code_p'], "le code P", ligne)
            msg += info
            donnee['centre'], info = VerifFormat.est_un_alphanumerique(donnee['centre'], "le centre financier", ligne)
            msg += info
            donnee['fonds'], info = VerifFormat.est_un_alphanumerique(donnee['fonds'], "les fonds à créditer", ligne)
            msg += info
            donnee['abrev_plat'], info = VerifFormat.est_un_alphanumerique(donnee['abrev_plat'], "l'abréviation", ligne)
            msg += info
            if donnee['abrev_plat'] not in abrevs:
                abrevs.append(donnee['abrev_plat'])
            else:
                msg += "l'abréviation plateforme de la ligne " + str(ligne) + " n'est pas unique \n"
            donnee['int_plat'], info = VerifFormat.est_un_texte(donnee['int_plat'], "l'intitulé", ligne)
            msg += info
            donnee['grille'], info = VerifFormat.est_un_document(donnee['grille'], "la grille tarifaire", ligne, True)
            msg += info
            if donnee['grille'] != "":
                if not Outils.existe(Outils.chemin([chemin_grille, donnee['grille'] + '.pdf'])):
                    msg += "la grille de la ligne " + str(ligne) + " n'existe pas dans le dossier d'entrée \n"

            donnees_dict[donnee['id_plateforme']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + msg)

        if edition.plateforme not in self.donnees.keys():
            Outils.fatal(ErreurConsistance(),
                         edition.libelle + "\n" + "l'id plateforme '" + edition.plateforme + "' n'est pas référencé\n")
