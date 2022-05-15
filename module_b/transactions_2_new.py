from core import (Format,
                  CsvDict)
from imports.construits import Transactions2


class Transactions2New(CsvDict):
    """
    Classe pour la création des transactions de niveau 2
    """

    def __init__(self, imports, transactions_3, par_client, numeros):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_client: tri des transactions
        :param numeros: table des numéros de version
        """
        super().__init__(imports)

        self.nom = "Transaction2_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"
        self.cles = Transactions2.cles

        i = 0
        for code, par_code in par_client.items():
            for icf in par_code['projets']:
                par_fact = par_code['projets'][icf]
                id_fact = numeros.couples[code][icf]
                for order, par_order in sorted(par_fact['articles'].items()):
                    for nbr, par_item in sorted(par_order.items()):
                        for par_user in par_item.values():
                            ligne = [imports.edition.annee, imports.edition.mois, imports.version, id_fact]
                            base = transactions_3.valeurs[par_user['base']]
                            if base['invoice-project'] == "0":
                                ligne.append("GLOB")
                            else:
                                ligne.append("CPTE")
                            for cle in range(5, 16):
                                ligne.append(base[self.cles[cle]])
                            ligne.append(base['user-name'] + " " + base['user-first'][0] + ".")
                            ligne += [par_user['start-y'], par_user['start-m'], par_user['end-y'], par_user['end-m']]
                            for cle in range(21, 28):
                                ligne.append(base[self.cles[cle]])
                            ligne += [round(par_user['quantity'], 3), base['item-unit'], base['valuation-price'],
                                      round(par_user['deduct'], 2), round(par_user['total'], 2)]
                            self._ajouter_valeur(ligne, i)
                            i += 1
