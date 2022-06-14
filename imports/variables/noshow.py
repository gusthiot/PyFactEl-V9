from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class NoShow(CsvImport):
    """
    Classe pour l'importation des données de No Show
    """

    cles = ['annee', 'mois', 'date_debut', 'type', 'id_machine', 'id_user', 'id_compte', 'penalite', 'validation',
            'id_staff']
    nom_fichier = "noshow.csv"
    libelle = "Pénalités No Show"

    def __init__(self, dossier_source, comptes, machines, users):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param comptes: comptes importés
        :param machines: machines importées
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

            msg += self._test_id_coherence(donnee['id_machine'], "l'id machine", ligne, machines)

            msg += self._test_id_coherence(donnee['id_user'], "l'id user", ligne, users)

            msg += self._test_id_coherence(donnee['id_staff'], "l'id staff", ligne, users, True)

            if donnee['type'] == "":
                msg += "HP/HC " + str(ligne) + " ne peut être vide\n"
            elif donnee['type'] != "HP" and donnee['type'] != "HC":
                msg += "HP/HC " + str(ligne) + " doit être égal à HP ou HC\n"

            donnee['penalite'], info = Format.est_un_nombre(donnee['penalite'], "la pénalité", ligne, 2, 0)
            msg += info

            donnee['date_debut'], info = Format.est_une_date(donnee['date_debut'], "la date de début", ligne)
            msg += info

            if donnee['validation'] not in ['0', '1', '2', '3']:
                msg += "la validation " + str(ligne) + " doit être parmi [0, 1, 2, 3]"

            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
