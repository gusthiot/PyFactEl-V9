from core import (Format, CsvDict)
from imports.construits import Granted


class GrantedNew(CsvDict):
    """
    Classe pour la création du listing des montants de subsides comptabilisés
    """

    def __init__(self, imports, transactions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        """
        super().__init__(imports)
        self.nom = "granted_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + ".csv"
        self.cles = Granted.cles

        for key in imports.grants.donnees.keys():
            self.valeurs[key] = imports.grants.donnees[key].copy()

        for key in transactions.comptabilises.keys():
            if key in self.valeurs.keys():
                self.valeurs[key]['subsid-alrdygrant'] = \
                    self.valeurs[key]['subsid-alrdygrant'] + transactions.comptabilises[key]['subsid-alrdygrant']
            else:
                self.valeurs[key] = transactions.comptabilises[key].copy()
