from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Version(CsvImport):
    """
    Classe pour l'importation des données des versions de facture
    """

    cles = ['invoice-id', 'client-code', 'invoice-type', 'version-last', 'version-change', 'version-old-amount',
            'version-new-amount']
    libelle = "Versions de facture"

    def __init__(self, dossier_source, annee, mois, version, module_a=False):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param annee: année du fichier ciblé
        :param mois: mois du fichier ciblé
        :param version: version de facturation ciblée
        :param module_a: si on ne traite que le module A
        """
        self.nom_fichier = "Table-versions-factures_" + str(annee) + "_" + Format.mois_string(mois) + \
                           "_" + str(version) + ".csv"
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}

        for donnee in self.donnees:
            donnee['invoice-id'], info = Format.est_un_entier(donnee['invoice-id'], "l'id facture", ligne, 1001)
            msg += info

            if module_a:
                donnee['client-code'], info = Format.est_un_entier(donnee['client-code'], "le code client", ligne, 0)
            else:
                donnee['client-code'], info = Format.est_un_alphanumerique(donnee['client-code'], "le code client",
                                                                           ligne)
            msg += info

            donnee['version-last'], info = Format.est_un_entier(donnee['version-last'], "la version", ligne, 0)
            msg += info

            if (donnee['version-change'] != 'NEW' and donnee['version-change'] != 'CANCELED' and
                    donnee['version-change'] != 'CORRECTED' and donnee['version-change'] != 'IDEM'):
                msg += "le version-change de la ligne " + str(ligne) + " doit être NEW, CANCELED, CORRECTED ou IDEM\n"

            donnee['version-old-amount'], info = Format.est_un_nombre(donnee['version-old-amount'], "l'ancien montant",
                                                                      ligne, 2, 0)
            msg += info
            donnee['version-new-amount'], info = Format.est_un_nombre(donnee['version-new-amount'],
                                                                      "le nouveau montant", ligne, 2, 0)
            msg += info

            donnees_dict[donnee['invoice-id']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
