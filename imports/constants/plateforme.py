from core import CsvImport
from core import (Interface,
                  Format,
                  Chemin,
                  ErreurConsistance)


class Plateforme(CsvImport):
    """
    Classe pour l'importation des données de Plateformes
    """

    nom_fichier = "plateforme.csv"
    cles = ['id_plateforme', 'code_p', 'centre', 'fonds', 'abrev_plat', 'int_plat', 'grille']
    libelle = "Plateformes"

    def __init__(self, dossier_source, clients, edition, chemin_grille, module_a=False):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param clients: clients importés
        :param edition: paramètres d'édition
        :param chemin_grille: dossier devant contenir la grille tarifaire
        :param module_a: si on ne traite que le module A
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 1
        donnees_dict = {}
        abrevs = []
        ids = []

        del self.donnees[0]
        for donnee in self.donnees:
            if module_a:
                donnee['id_plateforme'], info = Format.est_un_entier(donnee['id_plateforme'], "l'id plateforme", ligne,
                                                                     0)
            else:
                donnee['id_plateforme'], info = Format.est_un_alphanumerique(donnee['id_plateforme'], "l'id plateforme",
                                                                             ligne)
            msg += info
            if donnee['id_plateforme'] == "":
                msg += "l'id plateforme " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_plateforme'] not in clients.donnees.keys():
                msg += "l'id plateforme de la ligne " + str(ligne) + " n'existe pas dans les clients \n"
            elif donnee['id_plateforme'] not in ids:
                ids.append(donnee['id_plateforme'])
            else:
                msg += "l'id plateforme de la ligne " + str(ligne) + " n'est pas unique \n"

            donnee['code_p'], info = Format.est_un_alphanumerique(donnee['code_p'], "le code P", ligne)
            msg += info
            donnee['centre'], info = Format.est_un_alphanumerique(donnee['centre'], "le centre financier", ligne)
            msg += info
            donnee['fonds'], info = Format.est_un_alphanumerique(donnee['fonds'], "les fonds à créditer", ligne)
            msg += info
            donnee['abrev_plat'], info = Format.est_un_alphanumerique(donnee['abrev_plat'], "l'abréviation", ligne)
            msg += info
            if donnee['abrev_plat'] not in abrevs:
                abrevs.append(donnee['abrev_plat'])
            else:
                msg += "l'abréviation plateforme de la ligne " + str(ligne) + " n'est pas unique \n"
            donnee['int_plat'], info = Format.est_un_texte(donnee['int_plat'], "l'intitulé", ligne)
            msg += info
            donnee['grille'], info = Format.est_un_document(donnee['grille'], "la grille tarifaire", ligne, True)
            msg += info
            if donnee['id_plateforme'] == edition.plateforme and donnee['grille'] != "":
                if not Chemin.existe(Chemin.chemin([chemin_grille, donnee['grille'] + '.pdf'])):
                    msg += "la grille de la ligne " + str(ligne) + " n'existe pas dans le dossier d'entrée \n"

            donnees_dict[donnee['id_plateforme']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)

        if edition.plateforme not in self.donnees.keys():
            Interface.fatal(ErreurConsistance(),
                            edition.libelle + "\n" + "l'id plateforme '" + str(edition.plateforme) +
                            "' n'est pas référencé\n")
