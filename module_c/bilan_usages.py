from core import (Format,
                  CsvList)
import math


class BilanUsages(CsvList):
    """
    Classe pour la création du csv de bilan d'usage
    """

    cles = ['invoice-year', 'invoice-month', 'platf-code', 'platf-name', 'item-id', 'item-nbr', 'item-name',
            'item-unit', 'transac-usage', 'transac-runtime', 'runtime-N', 'runtime-avg', 'runtime-stddev']

    def __init__(self, imports, transactions_3, par_item):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_item: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Bilan-usage_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                   Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for tbtr in par_item.values():
            base = transactions_3.valeurs[tbtr[0]]
            if base['item-flag-usage'] == "OUI":
                ligne = [imports.edition.annee, imports.edition.mois]
                for cle in range(2, len(self.cles)-5):
                    ligne.append(base[self.cles[cle]])
                usage = 0
                runtime = 0
                nn = 0
                avg = 0
                stddev = 0
                rts = []
                for indice in tbtr:
                    trans = transactions_3.valeurs[indice]
                    usage += trans['transac-usage']
                    if trans['transac-runtime'] != "":
                        rti = trans['transac-runtime']
                        runtime += rti
                        nn += 1
                        rts.append(rti)
                if nn > 0:
                    avg = runtime / nn
                    somme = 0
                    for rt in rts:
                        somme += math.pow(rt-avg, 2)
                    stddev = math.sqrt(1 / nn * somme)
                ligne += [round(usage, 3), round(runtime, 3), nn, round(avg, 3), round(stddev, 3)]
                self.lignes.append(ligne)
