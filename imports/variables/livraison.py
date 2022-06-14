from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Livraison(CsvImport):
    """
    Classe pour l'importation des données de Livraisons
    """

    cles = ['annee', 'mois', 'id_compte', 'id_user', 'id_prestation', 'date_livraison', 'quantite', 'rabais',
            'id_operateur', 'id_livraison', 'date_commande', 'remarque', 'validation', 'id_staff']
    nom_fichier = "lvr.csv"
    libelle = "Livraison Prestations"

    def __init__(self, dossier_source, comptes, prestations, users):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param comptes: comptes importés
        :param prestations: prestations importées
        :param users: users importés
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_list = []
        coms = []

        for donnee in self.donnees:
            donnee['mois'], info = Format.est_un_entier(donnee['mois'], "le mois ", ligne, 1, 12)
            msg += info
            donnee['annee'], info = Format.est_un_entier(donnee['annee'], "l'annee ", ligne, 2000, 2099)
            msg += info

            info = self._test_id_coherence(donnee['id_compte'], "l'id compte", ligne, comptes)
            if info == "" and donnee['id_compte'] not in coms:
                coms.append(donnee['id_compte'])
            else:
                msg += info

            msg += self._test_id_coherence(donnee['id_prestation'], "l'id prestation", ligne, prestations)

            msg += self._test_id_coherence(donnee['id_user'], "l'id user", ligne, users)

            msg += self._test_id_coherence(donnee['id_operateur'], "l'id opérateur", ligne, users)

            msg += self._test_id_coherence(donnee['id_staff'], "l'id staff", ligne, users, True)

            donnee['quantite'], info = Format.est_un_nombre(donnee['quantite'], "la quantité", ligne, 1, 0)
            msg += info
            donnee['rabais'], info = Format.est_un_nombre(donnee['rabais'], "le rabais", ligne, 2, 0)
            msg += info

            donnee['date_livraison'], info = Format.est_une_date(donnee['date_livraison'], "la date de livraison",
                                                                 ligne)
            msg += info
            donnee['date_commande'], info = Format.est_une_date(donnee['date_commande'], "la date de commande", ligne)
            msg += info

            donnee['id_livraison'], info = Format.est_un_texte(donnee['id_livraison'], "l'id livraison", ligne)
            msg += info

            donnee['remarque'], info = Format.est_un_texte(donnee['remarque'], "la remarque", ligne, True)
            msg += info

            if donnee['validation'] not in ['0', '1', '2', '3']:
                msg += "la validation " + str(ligne) + " doit être parmi [0, 1, 2, 3]"

            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
