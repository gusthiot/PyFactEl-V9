from core import (Format,
                  CsvList)


class BilanFactures(CsvList):
    """
    Classe pour la création du bilan des factures
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-id', 'invoice-ref', 'platf-name',
            'client-code', 'client-sap', 'client-name', 'client-idclass', 'client-class', 'client-labelclass',
            'total-fact']

    def __init__(self, imports, transactions_1, sommes_1):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_1: transactions 1 générées
        :param sommes_1: sommes des transactions 1
        """
        super().__init__(imports)

        self.nom = "Bilan-factures_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for id_fact in sommes_1.par_fact.keys():
            par_fact = sommes_1.par_fact[id_fact]['transactions']['keys']
            base = transactions_1.valeurs[par_fact[0]]
            total = sommes_1.par_fact[id_fact]['transactions']['total']

            ligne = []
            for cle in self.cles:
                if cle == 'total-fact':
                    ligne.append(round(2*total, 1)/2)
                else:
                    ligne.append(base[cle])
            self.lignes.append(ligne)
