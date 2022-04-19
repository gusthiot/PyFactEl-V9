from core import (Format,
                  CsvList)
import math


class StatMachine(CsvList):
    """
    Classe pour la création du csv des stats nombre user
    """

    cles = ['invoice-year', 'invoice-month', 'mach-id', 'mach-name', 'item-id', 'flow-type', 'item-codeK', 'item-textK',
            'item-nbr', 'item-name', 'item-unit', 'transac-quantity', 'transac-usage', 'transac-runtime', 'runtime-N',
            'runtime-avg', 'runtime-stddev']

    def __init__(self, imports, transactions, par_machine):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_machine: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Stat-machine_" + str(imports.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + "_" \
                   + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for id_machine in par_machine.keys():
            for item in par_machine[id_machine]:
                ligne = [imports.edition.annee, imports.edition.mois]
                tbtr = par_machine[id_machine][item]
                base = transactions.valeurs[tbtr[0]]
                for cle in range(2, len(self.cles)-6):
                    ligne.append(base[self.cles[cle]])
                quantity = 0
                usage = 0
                runtime = 0
                nn = 0
                avg = 0
                stddev = 0
                rts = []
                for indice in tbtr:
                    trans = transactions.valeurs[indice]
                    quantity += trans['transac-quantity']
                    usage += trans['transac-usage']
                    run = trans['transac-runtime']
                    if run != "":
                        runtime += run
                        rts.append(run)
                        nn += 1
                if nn > 0:
                    avg = runtime / nn
                    somme = 0
                    for rt in rts:
                        somme += math.pow(rt-avg, 2)
                    stddev = math.sqrt(1 / nn * somme)
                ligne += [round(quantity, 4), round(usage, 4), round(runtime, 4), nn, round(avg, 4),
                          round(stddev, 4)]
                self.lignes.append(ligne)
