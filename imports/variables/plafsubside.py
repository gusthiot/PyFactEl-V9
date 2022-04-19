from imports import Fichier
from core import (Interface,
                  Format,
                  ErreurConsistance)


class PlafSubside(Fichier):
    """
    Classe pour l'importation des données ded Plafonds de Subsides
    """

    nom_fichier = "plafsubside.csv"
    cles = ['type', 'id_plateforme', 'id_article', 'pourcentage', 'max_mois', 'max_compte']
    libelle = "Plafonds Subsides"

    def __init__(self, dossier_source, subsides, artsap, plateformes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param subsides: subsides importés
        :param artsap: articles SAP importés
        :param plateformes: plateformes importées
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        triplets = []

        for donnee in self.donnees:
            msg += self._test_id_coherence(donnee['type'], "le type", ligne, subsides)

            msg += self._test_id_coherence(donnee['id_article'], "l'id article SAP", ligne, artsap)

            msg += self._test_id_coherence(donnee['id_plateforme'], "l'id plateforme", ligne, plateformes)

            triplet = [donnee['type'], donnee['id_plateforme'], donnee['id_article']]
            if triplet not in triplets:
                triplets.append(triplet)
            else:
                msg += "Triplet type '" + donnee['type'] + "' id plateforme '" + donnee['id_plateforme'] + \
                       "' et id article SAP '" + donnee['id_article'] + "' de la ligne " + str(ligne) + " pas unique\n"

            donnee['pourcentage'], info = Format.est_un_nombre(donnee['pourcentage'], "le pourcentage", ligne, 2, 0,
                                                               100)
            msg += info

            donnee['max_mois'], info = Format.est_un_nombre(donnee['max_mois'], "le max mensuel", ligne, 2, 0)
            msg += info

            donnee['max_compte'], info = Format.est_un_nombre(donnee['max_compte'], "le max compte", ligne, 2, 0)
            msg += info

            donnees_dict[donnee['type'] + donnee['id_plateforme'] + donnee['id_article']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
