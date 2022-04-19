from imports import Fichier
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Granted(Fichier):
    """
    Classe pour l'importation des données de Subsides comptabilisés
    """

    cles = ['proj-id', 'platf-code', 'item-idsap', 'subsid-alrdygrant']
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
            self.nom_fichier = "granted_" + str(edition.annee) + "_" + Format.mois_string(edition.mois-1) + ".csv"
        else:
            self.nom_fichier = "granted_" + str(edition.annee-1) + "_" + Format.mois_string(12) + ".csv"
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        triplets = []

        for donnee in self.donnees:
            msg += self._test_id_coherence(donnee['proj-id'], "l'id compte", ligne, comptes)

            msg += self._test_id_coherence(donnee['item-idsap'], "l'id article SAP", ligne, artsap)

            msg += self._test_id_coherence(donnee['platf-code'], "l'id plateforme", ligne, plateformes)

            triplet = [donnee['proj-id'], donnee['platf-code'], donnee['item-idsap']]
            if triplet not in triplets:
                triplets.append(triplet)
            else:
                msg += "Triplet type '" + donnee['type'] + "' id plateforme '" + donnee['platf-code'] + \
                       "' et id article SAP '" + donnee['item-idsap'] + "' de la ligne " + str(ligne) + " pas unique\n"

            donnee['subsid-alrdygrant'], info = Format.est_un_nombre(donnee['subsid-alrdygrant'],
                                                                     "le montant comptabilisé", ligne, 2, 0)
            msg += info

            donnees_dict[donnee['proj-id'] + donnee['platf-code'] + donnee['item-idsap']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
