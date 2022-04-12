from imports import Fichier
from core import (Outils,
                  VerifFormat,
                  ErreurConsistance)


class ArticleSap(Fichier):
    """
    Classe pour l'importation des données des Articles SAP
    """

    cles = ['id_article', 'code_d', 'flag_usage', 'flag_conso', 'eligible', 'ordre', 'intitule', 'code_sap',
            'quantite', 'unite', 'type_prix', 'type_rabais', 'texte_sap']
    nom_fichier = "articlesap.csv"
    libelle = "Articles SAP"

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        super().__init__(dossier_source)
        self.id_d1 = None
        self.id_d2 = None
        self.ids_d3 = []

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_article'], info = VerifFormat.est_un_alphanumerique(donnee['id_article'], "l'id article SAP",
                                                                           ligne)
            msg += info
            if info == "":
                if donnee['id_article'] not in ids:
                    ids.append(donnee['id_article'])
                else:
                    msg += "l'id article SAP '" + donnee['id_article'] + "' de la ligne " + str(ligne) +\
                           " n'est pas unique\n"

            donnee['code_d'], info = VerifFormat.est_un_alphanumerique(donnee['code_d'], "le code D", ligne)
            msg += info
            donnee['intitule'], info = VerifFormat.est_un_texte(donnee['intitule'], "l'intitulé", ligne)
            msg += info
            donnee['code_sap'], info = VerifFormat.est_un_entier(donnee['code_sap'], "le code sap", ligne, 1)
            msg += info
            donnee['quantite'], info = VerifFormat.est_un_nombre(donnee['quantite'], "la quantité", ligne, 3, 0)
            msg += info
            donnee['unite'], info = VerifFormat.est_un_texte(donnee['unite'], "l'unité", ligne)
            msg += info
            donnee['ordre'], info = VerifFormat.est_un_entier(donnee['ordre'], "l'ordre annexe", ligne, 1)
            msg += info
            donnee['type_prix'], info = VerifFormat.est_un_alphanumerique(donnee['type_prix'], "le type de prix", ligne)
            msg += info
            donnee['type_rabais'], info = VerifFormat.est_un_alphanumerique(donnee['type_rabais'], "le type de rabais",
                                                                            ligne)
            msg += info
            donnee['texte_sap'], info = VerifFormat.est_un_texte(donnee['texte_sap'], "le texte sap", ligne, True)
            msg += info
            if donnee['flag_usage'] != 'OUI' and donnee['flag_usage'] != 'NON':
                msg += "le flag usage de la ligne " + str(ligne) + " doit être OUI ou NON\n"
            if donnee['flag_conso'] != 'OUI' and donnee['flag_conso'] != 'NON':
                msg += "le flag conso de la ligne " + str(ligne) + " doit être OUI ou NON\n"
            if donnee['eligible'] != 'OUI' and donnee['eligible'] != 'NON':
                msg += "l'éligible de la ligne " + str(ligne) + " doit être OUI ou NON\n"

            if donnee['code_d'] == 'C' or donnee['code_d'] == 'X':
                self.ids_d3.append(donnee['id_article'])
            elif donnee['code_d'] == 'M':
                self.id_d1 = donnee['id_article']
            elif donnee['code_d'] == 'R':
                self.id_d2 = donnee['id_article']
            else:
                msg += "le code D de la ligne " + str(ligne) + " doit être M, R, C ou X\n"

            donnees_dict[donnee['id_article']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
