from core import (Format,
                  CsvDict)


class Transactions1(CsvDict):
    """
    Classe pour la création des transactions de niveau 1
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-id', 'invoice-ref', 'platf-name',
            'client-code', 'client-sap', 'client-name', 'client-idclass', 'client-class', 'client-labelclass',
            'proj-id', 'proj-nbr', 'proj-name', 'item-idsap', 'item-codeD', 'item-order', 'item-labelcode',
            'total-fact']

    def __init__(self, imports, transactions_2, sommes_2):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_2: transactions 2 générées
        :param sommes_2: sommes des transactions 2
        """
        super().__init__(imports)

        self.nom = "Transaction1_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        i = 0
        for id_fact, par_fact in sommes_2.par_fact.items():
            for par_compte in par_fact['projets'].values():
                for par_article in par_compte.values():
                    base = None
                    total = 0
                    for par_item in par_article.values():
                        for par_user in par_item.values():
                            for key in par_user:
                                trans = transactions_2.valeurs[key]
                                if not base:
                                    base = trans
                                total += trans['total-fact']

                    ligne = []
                    code = base['client-code']
                    client = imports.clients.donnees[code]
                    id_classe = client['id_classe']
                    classe = imports.classes.donnees[id_classe]
                    ref = classe['ref_fact'] + "_" + str(imports.edition.annee) + "_" + \
                          Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(id_fact)
                    for cle in self.cles:
                        if cle == 'invoice-ref':
                            ligne.append(ref)
                        elif cle == 'total-fact':
                            ligne.append(round(2*total, 1)/2)
                        else:
                            ligne.append(base[cle])
                    self._ajouter_valeur(ligne, i)
                    i += 1
