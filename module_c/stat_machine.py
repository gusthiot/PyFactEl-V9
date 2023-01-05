from core import (Format,
                  CsvList)
import math


class StatMachine(CsvList):
    """
    Classe pour la création du csv des stats nombre user
    """

    cles = ['year', 'month', 'mach-id', 'mach-name', 'item-id', 'flow-type', 'item-codeK', 'item-textK',
            'item-nbr', 'item-name', 'item-unit', 'transac-quantity', 'transac-usage', 'transac-runtime', 'runtime-N',
            'runtime-avg', 'runtime-stddev']

    def __init__(self, imports, transactions_3, par_machine):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_machine: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Stat-machine_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" \
                   + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for pmi in par_machine.values():
            for par_item in pmi.values():
                ligne = [imports.edition.annee, imports.edition.mois]
                base = transactions_3.valeurs[par_item['base']]
                for cle in range(2, len(self.cles)-6):
                    ligne.append(base[self.cles[cle]])
                runtime = par_item['runtime']
                nn = par_item['nn']
                avg = 0
                stddev = 0
                rts = par_item['rts']
                if nn > 0:
                    avg = runtime / nn
                    somme = 0
                    for rt in rts:
                        somme += math.pow(rt-avg, 2)
                    stddev = math.sqrt(1 / nn * somme)
                ligne += [round(par_item['quantity'], 3), round(par_item['usage'], 3), round(runtime, 3), nn,
                          round(avg, 3), round(stddev, 3)]
                self.lignes.append(ligne)
