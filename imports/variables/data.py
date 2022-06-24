from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Data(CsvImport):
    """
    Classe pour l'importation des données de Data pour module A uniquement
    """

    cles = ['invoice-year', 'invoice-month', 'client-code', 'proj-id', 'proj-nbr', 'proj-name', 'user-id', 'user-name',
            'date-start-y', 'date-start-m', 'date-end-y', 'date-end-m', 'item-idsap', 'item-id', 'item-nbr',
            'item-name', 'transac-quantity', 'item-unit', 'valuation-price', 'deduct-CHF']
    nom_fichier = "data.csv"
    libelle = "DATA"

    def __init__(self, dossier_source, clients, artsap):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param clients: clients importés
        :param artsap: articles SAP importés
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_list = []
        septuplets = []

        for donnee in self.donnees:
            donnee['invoice-month'], info = Format.est_un_entier(donnee['invoice-month'], "le mois ", ligne, 1, 12)
            msg += info
            donnee['invoice-year'], info = Format.est_un_entier(donnee['invoice-year'], "l'annee ", ligne, 2000, 2099)
            msg += info
            donnee['client-code'], info = Format.est_un_entier(donnee['client-code'], "le code client", ligne, 0)
            msg += info
            donnee['proj-id'], info = Format.est_un_alphanumerique(donnee['proj-id'], "l'id projet", ligne)
            msg += info
            donnee['user-id'], info = Format.est_un_alphanumerique(donnee['user-id'], "l'id user", ligne)
            msg += info
            donnee['item-idsap'], info = Format.est_un_alphanumerique(donnee['item-idsap'], "l'id article", ligne)
            msg += info
            donnee['item-id'], info = Format.est_un_alphanumerique(donnee['item-id'], "l'id item", ligne)
            msg += info
            donnee['date-start-m'], info = Format.est_un_entier(donnee['date-start-m'], "le mois de départ", ligne, 1,
                                                                12)
            msg += info
            donnee['date-start-y'], info = Format.est_un_entier(donnee['date-start-y'], "l'annee de départ", ligne,
                                                                2000, 2099)
            msg += info
            donnee['date-end-m'], info = Format.est_un_entier(donnee['date-end-m'], "le mois de fin", ligne, 1, 12)
            msg += info
            donnee['date-end-y'], info = Format.est_un_entier(donnee['date-end-y'], "l'annee de fin", ligne, 2000, 2099)
            msg += info
            donnee['transac-quantity'], info = Format.est_un_nombre(donnee['transac-quantity'], "la quantité", ligne,
                                                                    mini=0)
            msg += info
            donnee['valuation-price'], info = Format.est_un_nombre(donnee['valuation-price'], "le prix unitaire", ligne,
                                                                    mini=0)
            msg += info
            donnee['deduct-CHF'], info = Format.est_un_nombre(donnee['deduct-CHF'], "la déduction", ligne, mini=0)
            msg += info
            msg += self._test_id_coherence(donnee['client-code'], "le code client", ligne, clients)
            msg += self._test_id_coherence(donnee['item-idsap'], "l'id article SAP", ligne, artsap)

            septuplet = [donnee['invoice-year'], donnee['invoice-month'], donnee['client-code'], donnee['proj-id'],
                         donnee['user-id'], donnee['item-idsap'], donnee['item-id']]
            if septuplet not in septuplets:
                septuplets.append(septuplet)
            else:
                msg += "Septuplet année '" + donnee['invoice-year'] + "' mois '" + donnee['invoice-month'] + \
                       "' id client '" + donnee['client-code'] + "' id compte '" + donnee['proj-id'] + \
                       "' id user '" + donnee['user-id'] + "' id article SAP '" + donnee['id_article'] + \
                       "' et id item '" + donnee['item-id'] + "' de la ligne " + str(ligne) + " pas unique\n"

            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
