from imports import Fichier
from core import (Outils,
                  ErreurConsistance)


class UserLabo(Fichier):
    """
    Classe pour l'importation des données des Utilisateurs des  laboratoires
    """

    cles = ['year', 'month', 'day', 'week-nbr', 'platf-code', 'platf-op', 'platf-name', 'client-code', 'client-name',
            'client-class', 'user-id', 'user-sciper', 'user-name', 'user-first']
    libelle = "User labo"

    def __init__(self, dossier_source, edition, plateformes, clients, users):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param edition: paramètres d'édition
        :param plateformes: plateformes importées
        :param clients: clients importés
        :param users: users importés
        """
        if edition.mois > 1:
            self.nom_fichier = "User-labo_" + str(edition.annee) + "_" + Outils.mois_string(edition.mois-1) + ".csv"
        else:
            self.nom_fichier = "User-labo_" + str(edition.annee-1) + "_" + Outils.mois_string(12) + ".csv"
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_list = []

        for donnee in self.donnees:
            msg += self._test_id_coherence(donnee['platf-code'], "l'id plateforme", ligne, plateformes)

            msg += self._test_id_coherence(donnee['client-code'], "le code client", ligne, clients)

            msg += self._test_id_coherence(donnee['user-id'], "l'id user", ligne, users)

            donnees_list.append(donnee)
            ligne += 1

        self.donnees = donnees_list

        if msg != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
