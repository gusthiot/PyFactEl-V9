from core import (Format,
                  CsvList)


class NumeroNew(CsvList):
    """
    Classe pour la création de la table des numéros de facture
    """

    def __init__(self, imports, transactions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        """
        super().__init__(imports)
        self.nom = "Table-numeros-factures_" + str(imports.edition.annee) + "_" + \
                   Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"
        self.couples = {}
        id_facture = 1000
        if imports.version > 0:
            for key in imports.numeros.donnees.keys():
                numero = imports.numeros.donnees[key]
                if key > id_facture:
                    id_facture = key
                code = numero['client-code']
                icf = numero['invoice-project']
                if code not in self.couples:
                    self.couples[code] = {}
                self.couples[code][icf] = key
                self.lignes.append([key, code, icf])

        for key in transactions.valeurs.keys():
            transaction = transactions.valeurs[key]
            if (imports.edition.annee == transaction['invoice-year'] and
                    imports.edition.mois == transaction['invoice-month']):
                code = transaction['client-code']
                icf = transaction['invoice-project']
                if code not in self.couples:
                    self.couples[code] = {}
                if icf not in self.couples[code]:
                    id_facture = id_facture + 1
                    self.couples[code][icf] = id_facture
                    self.lignes.append([id_facture, code, icf])
