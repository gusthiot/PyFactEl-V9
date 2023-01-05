from core import (Format, CsvList)


class BilanConsos(CsvList):
    """
    Classe pour la création du csv de bilan de consommation propre
    """

    cles = ['year', 'month', 'platf-code', 'platf-name', 'proj-id', 'proj-nbr', 'proj-name',
            'proj-expl', 'item-id', 'item-nbr', 'item-name', 'item-unit', 'item-idsap', 'item-codeD', 'item-extra',
            'mach-extra', 'conso-propre-march-expl', 'conso-propre-extra-expl', 'conso-propre-march-proj',
            'conso-propre-extra-proj']

    def __init__(self, imports, transactions_3, par_projet):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_projet: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Bilan-conso-propre_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for ppi in par_projet.values():
            for par_item in ppi.values():
                base = transactions_3.valeurs[par_item['base']]
                if base['item-flag-conso'] == "OUI":
                    ligne = [imports.edition.annee, imports.edition.mois]
                    for cle in range(2, len(self.cles) - 4):
                        ligne.append(base[self.cles[cle]])
                    goops = par_item['goops']
                    extrops = par_item['extrops']
                    goint = par_item['goint']
                    extrint = par_item['extrint']
                    if goops > 0 or extrops > 0 or goint > 0 or extrint > 0:
                        ligne += [round(goops, 2), round(extrops, 2), round(goint, 2), round(extrint, 2)]
                        self.lignes.append(ligne)
