from core import (Format,
                  CsvList)


class BilanSubsides(CsvList):
    """
    Classe pour la création du csv de bilan subsides
    """

    cles = ['invoice-year', 'invoice-month', 'platf-code', 'platf-name', 'client-code', 'client-sap', 'client-name',
            'client-idclass', 'client-class', 'client-labelclass', 'item-idsap', 'item-codeD', 'item-labelcode',
            'valuation-brut', 'valuation-net', 'deduct-CHF', 'subsid-deduct', 'total-fact', 'discount-bonus',
            'subsid-bonus']

    def __init__(self, imports, transactions_3, par_client):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_client: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Bilan-subsides_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for par_code in par_client.values():
            for par_article in par_code['articles'].values():
                base = transactions_3.valeurs[par_article['base']]
                ligne = [imports.edition.annee, imports.edition.mois]
                for cle in range(2, len(self.cles)-7):
                    ligne.append(base[self.cles[cle]])
                ligne += [round(par_article['avant'], 2), round(par_article['compris'], 2),
                          round(par_article['deduit'], 2), round(par_article['sub_ded'], 2),
                          round(par_article['fact'], 2), round(par_article['remb'], 2),
                          round(par_article['sub_remb'], 2)]
                self.lignes.append(ligne)
