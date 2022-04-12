from imports import Fichier
from core import (Outils,
                  VerifFormat,
                  ErreurConsistance)


class Granted(Fichier):
    """
    Classe pour l'importation des données de Subsides comptabilisés
    """

    cles = ['id_compte', 'id_plateforme', 'id_article', 'montant']
    libelle = "Subsides comptabilisés"

    def __init__(self, dossier_source, edition, comptes, artsap, plateformes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param comptes: comptes importés
        :param artsap: articles SAP importés
        :param plateformes: plateformes importées
        """
        if edition.mois > 1:
            self.nom_fichier = "granted_" + str(edition.annee) + "_" + Outils.mois_string(edition.mois-1) + ".csv"
        else:
            self.nom_fichier = "granted_" + str(edition.annee-1) + "_" + Outils.mois_string(12) + ".csv"
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        triplets = []

        for donnee in self.donnees:
            msg += self._test_id_coherence(donnee['id_compte'], "l'id compte", ligne, comptes)

            msg += self._test_id_coherence(donnee['id_article'], "l'id article SAP", ligne, artsap)

            msg += self._test_id_coherence(donnee['id_plateforme'], "l'id plateforme", ligne, plateformes)

            triplet = [donnee['id_compte'], donnee['id_plateforme'], donnee['id_article']]
            if triplet not in triplets:
                triplets.append(triplet)
            else:
                msg += "Triplet type '" + donnee['type'] + "' id plateforme '" + donnee['id_plateforme'] + \
                       "' et id article SAP '" + donnee['id_article'] + "' de la ligne " + str(ligne) + " pas unique\n"

            donnee['montant'], info = VerifFormat.est_un_nombre(donnee['montant'], "le montant comptabilisé", ligne, 2,
                                                                0)
            msg += info

            donnees_dict[donnee['id_compte'] + donnee['id_plateforme'] + donnee['id_article']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
