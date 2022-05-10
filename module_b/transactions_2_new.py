from core import (Format,
                  CsvDict)
from imports.construits import Transactions2


class Transactions2New(CsvDict):
    """
    Classe pour la création des transactions de niveau 2
    """

    def __init__(self, imports, transactions, par_client, numeros):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_client: tri des transactions
        :param numeros: table des numéros de version
        """
        super().__init__(imports)

        self.nom = "Transaction2_" + str(imports.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"
        self.cles = Transactions2.cles

        i = 0
        for code, par_code in par_client.items():
            for icf in par_code['projets']:
                par_fact = par_code['projets'][icf]
                id_fact = numeros.couples[code][icf]
                for order in sorted(par_fact['articles'].keys()):
                    par_order = par_fact['articles'][order]
                    for nbr in sorted(par_order.keys()):
                        par_item = par_order[nbr]
                        for tbtr in par_item.values():
                            ligne = [imports.edition.annee, imports.edition.mois, imports.version, id_fact]
                            base = transactions.valeurs[tbtr[0]]
                            if base['invoice-project'] == "0":
                                ligne.append("GLOB")
                            else:
                                ligne.append("CPTE")
                            for cle in range(5, 16):
                                ligne.append(base[self.cles[cle]])
                            ligne.append(base['user-name'] + " " + base['user-first'][0] + ".")
                            start_year = base['transac-date'].year
                            start_month = base['transac-date'].month
                            end_year = base['transac-date'].year
                            end_month = base['transac-date'].month
                            quantity = 0
                            deduct = 0
                            total = 0
                            for indice in tbtr:
                                trans = transactions.valeurs[indice]
                                quantity += trans['transac-quantity']
                                deduct += trans['deduct-CHF']
                                total += trans['total-fact']
                                if trans['transac-date'].year < start_year:
                                    start_year = trans['transac-date'].year
                                if trans['transac-date'].year > end_year:
                                    end_year = trans['transac-date'].year
                                if trans['transac-date'].month < start_month:
                                    start_month = trans['transac-date'].month
                                if trans['transac-date'].month > end_month:
                                    end_month = trans['transac-date'].month

                            ligne += [start_year, start_month, end_year, end_month]
                            for cle in range(21, 28):
                                ligne.append(base[self.cles[cle]])
                            ligne += [round(quantity, 3), base['item-unit'], base['valuation-price'], round(deduct, 2),
                                      round(total, 2)]
                            self._ajouter_valeur(ligne, i)
                            i += 1
