from imports import Fichier
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Categorie(Fichier):
    """
    Classe pour l'importation des données de Catégories
    """

    cles = ['id_categorie', 'no_categorie', 'intitule', 'unite', 'id_plateforme', 'id_article']
    nom_fichier = "categorie.csv"
    libelle = "Catégories"

    def __init__(self, dossier_source, artsap, plateformes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param artsap: articles SAP importés
        :param plateformes: plateformes importées
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_categorie'], info = Format.est_un_alphanumerique(donnee['id_categorie'], "l'id catégorie", ligne)
            msg += info
            if info == "":
                if donnee['id_categorie'] not in ids:
                    ids.append(donnee['id_categorie'])
                else:
                    msg += "l'id catégorie '" + donnee['id_categorie'] + "' de la ligne " + str(ligne) +\
                           " n'est pas unique\n"

            msg += self._test_id_coherence(donnee['id_article'], "l'id article SAP", ligne, artsap)

            msg += self._test_id_coherence(donnee['id_plateforme'], "l'id plateforme", ligne, plateformes)

            donnee['no_categorie'], info = Format.est_un_alphanumerique(donnee['no_categorie'], "le no catégorie",
                                                                        ligne)
            msg += info
            donnee['intitule'], info = Format.est_un_texte(donnee['intitule'], "l'intitulé", ligne)
            msg += info
            donnee['unite'], info = Format.est_un_texte(donnee['unite'], "l'unité", ligne)
            msg += info

            donnees_dict[donnee['id_categorie']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
