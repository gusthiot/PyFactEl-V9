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
            for tbtr in par_code['articles'].values():
                base = transactions_3.valeurs[tbtr[0]]
                ligne = [imports.edition.annee, imports.edition.mois]
                for cle in range(2, len(self.cles)-7):
                    ligne.append(base[self.cles[cle]])
                avant = 0
                compris = 0
                deduit = 0
                sub_ded = 0
                fact = 0
                remb = 0
                sub_remb = 0
                for indice in tbtr:
                    val = transactions_3.valeurs[indice]
                    avant += val['valuation-brut']
                    compris += val['valuation-net']
                    deduit += val['deduct-CHF']
                    sub_ded += val['subsid-deduct']
                    fact += val['total-fact']
                    remb += val['discount-bonus']
                    sub_remb += val['subsid-bonus']
                ligne += [round(avant, 2), round(compris, 2), round(deduit, 2), round(sub_ded, 2), round(fact, 2),
                          round(remb, 2), round(sub_remb, 2)]
                self.lignes.append(ligne)
