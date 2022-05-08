from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Transactions2(CsvImport):
    """
    Classe pour l'importation des données des numéros de facture
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-id', 'invoice-type', 'platf-name',
            'client-code', 'client-sap', 'client-name', 'client-idclass', 'client-class', 'client-labelclass',
            'proj-id', 'proj-nbr', 'proj-name', 'user-id', 'user-name-f', 'date-start-y', 'date-start-m', 'date-end-y',
            'date-end-m', 'item-idsap', 'item-codeD', 'item-order', 'item-labelcode', 'item-id', 'item-nbr',
            'item-name', 'transac-quantity', 'item-unit', 'valuation-price', 'deduct-CHF', 'total-fact']
    libelle = "Versions de facture"

    def __init__(self, dossier_source, annee, mois, plateforme, version):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param annee: année du fichier ciblé
        :param mois: mois du fichier ciblé
        :param plateforme: plateforme traitée
        :param version: version de facturation ciblée
        """
        self.nom_fichier = "Transaction2_" + str(plateforme['abrev_plat']) + "_" + str(annee) + "_" + \
                           Format.mois_string(mois) + "_" + str(version) + ".csv"
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = {}

        for donnee in self.donnees:
            donnee['invoice-month'], info = Format.est_un_entier(donnee['invoice-month'], "le mois ", ligne, 1, 12)
            msg += info
            donnee['invoice-year'], info = Format.est_un_entier(donnee['invoice-year'], "l'annee ", ligne, 2000, 2099)
            msg += info
            donnee['invoice-version'], info = Format.est_un_entier(donnee['invoice-version'], "la version", ligne, 0)
            msg += info
            donnee['invoice-id'], info = Format.est_un_entier(donnee['invoice-id'], "l'id facture", ligne, 1001)
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
            donnee['total-fact'], info = Format.est_un_nombre(donnee['total-fact'], "le montant total", ligne, 2, 0)
            msg += info
            if donnee['invoice-id'] not in ids:
                ids[donnee['invoice-id']] = donnee['client-code']
            else:
                if donnee['client-code'] != ids[donnee['invoice-id']]:
                    msg += "l'id facture '" + donnee['invoice-id'] + "' de la ligne " + str(ligne) + \
                           " ne peut concerner 2 clients : " + ids[donnee['invoice-id']] + " et " + \
                           donnee['client-code'] + "\n"

            donnees_dict[ligne-1] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
