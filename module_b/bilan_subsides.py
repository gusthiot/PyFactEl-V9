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

    def __init__(self, imports, transactions, par_client):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_client: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Bilan-subsides_" + str(imports.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for code in par_client.keys():
            par_code = par_client[code]['articles']
            for code_d in par_code.keys():
                tbtr = par_code[code_d]
                base = transactions.valeurs[tbtr[0]]
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
                    val = transactions.valeurs[indice]
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
