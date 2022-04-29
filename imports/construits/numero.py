from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Numero(CsvImport):
    """
    Classe pour l'importation des données des numéros de facture
    """

    cles = ['invoice-id', 'client-code', 'invoice-project']
    libelle = "Numéros de facture"

    def __init__(self, dossier_source, edition, comptes, clients, version):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param comptes: comptes importés
        :param clients: clients importés
        :param version: version de facturation
        """
        self.nom_fichier = "Table-numeros-factures_" + str(edition.annee) + "_" + Format.mois_string(edition.mois) + \
                           "_" + str(version) + ".csv"
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}

        for donnee in self.donnees:
            msg += self._test_id_coherence(donnee['invoice-project'], "l'invoice-project", ligne, comptes, True)

            msg += self._test_id_coherence(donnee['client-code'], "le code client", ligne, clients)

            donnee['invoice-id'], info = Format.est_un_entier(donnee['invoice-id'], "l'id facture", ligne, 1001)
            msg += info

            donnees_dict[donnee['invoice-id']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
