from imports import Fichier
from core import (Outils,
                  VerifFormat,
                  ErreurConsistance)


class Service(Fichier):
    """
    Classe pour l'importation des données de Services
    """

    cles = ['annee', 'mois', 'id_compte', 'id_user', 'id_categorie', 'date', 'quantite', 'id_op', 'remarque_staff']
    nom_fichier = "srv.csv"
    libelle = "Services"

    def __init__(self, dossier_source, comptes, categories, users):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param comptes: comptes importés
        :param categories: catégories importées
        :param users: users importés
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_list = []
        coms = []

        for donnee in self.donnees:
            donnee['mois'], info = VerifFormat.est_un_entier(donnee['mois'], "le mois ", ligne, 1, 12)
            msg += info
            donnee['annee'], info = VerifFormat.est_un_entier(donnee['annee'], "l'annee ", ligne, 2000, 2099)
            msg += info

            info = self._test_id_coherence(donnee['id_compte'], "l'id compte", ligne, comptes)
            if info == "" and donnee['id_compte'] not in coms:
                coms.append(donnee['id_compte'])
            else:
                msg += info

            msg += self._test_id_coherence(donnee['id_categorie'], "l'id catégorie", ligne, categories)

            msg += self._test_id_coherence(donnee['id_user'], "l'id user", ligne, users)

            msg += self._test_id_coherence(donnee['id_op'], "l'id opérateur", ligne, users)

            donnee['quantite'], info = VerifFormat.est_un_nombre(donnee['quantite'], "la quantité", ligne, 3, 0)
            msg += info

            donnee['date'], info = VerifFormat.est_une_date(donnee['date'], "la date", ligne)
            msg += info

            donnee['remarque_staff'], info = VerifFormat.est_un_texte(donnee['remarque_staff'], "la remarque staff",
                                                                      ligne, True)
            msg += info

            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        if msg != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
