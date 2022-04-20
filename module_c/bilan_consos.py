from core import (Format, CsvList)


class BilanConsos(CsvList):
    """
    Classe pour la création du csv de bilan de consommation propre
    """

    cles = ['invoice-year', 'invoice-month', 'platf-code', 'platf-name', 'proj-id', 'proj-nbr', 'proj-name',
            'proj-expl', 'item-id', 'item-nbr', 'item-name', 'item-unit', 'item-idsap', 'item-codeD', 'item-extra',
            'mach-extra', 'conso-propre-march-expl', 'conso-propre-extra-expl', 'conso-propre-march-proj',
            'conso-propre-extra-proj']

    def __init__(self, imports, transactions, par_projet):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_projet: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Bilan-conso-propre_" + str(imports.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for par_item in par_projet.values():
            for tbtr in par_item.values():
                base = transactions.valeurs[tbtr[0]]
                if base['item-flag-conso'] == "OUI":
                    ligne = [imports.edition.annee, imports.edition.mois]
                    for cle in range(2, len(self.cles) - 4):
                        ligne.append(base[self.cles[cle]])
                    goops = 0
                    extrops = 0
                    goint = 0
                    extrint = 0
                    for indice in tbtr:
                        trans = transactions.valeurs[indice]
                        net = trans['valuation-net']
                        if trans['client-code'] == trans['platf-code']:
                            if trans['item-extra'] == "TRUE":
                                if trans['proj-expl'] == "TRUE":
                                    extrops += net
                                else:
                                    extrint += net
                            else:
                                if trans['proj-expl'] == "TRUE":
                                    goops += net
                                else:
                                    goint += net
                    if goops > 0 or extrops > 0 or goint > 0 or extrint > 0:
                        ligne += [round(goops, 2), round(extrops, 2), round(goint, 2), round(extrint, 2)]
                        self.lignes.append(ligne)
