from core import (Format,
                  CsvList)


class BilanFactures(CsvList):
    """
    Classe pour la création du bilan des factures
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-id', 'invoice-ref', 'platf-name',
            'client-code', 'client-sap', 'client-name', 'client-idclass', 'client-class', 'client-labelclass',
            'total-fact']

    def __init__(self, imports, transactions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param versions: versions des factures générées
        """
        super().__init__(imports)

        self.nom = "Bilan-factures_" + str(imports.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        trans_fact = {}
        for key, trans in transactions.valeurs.items():
            if trans['invoice-id'] not in trans_fact:
                trans_fact[trans['invoice-id']] = []
            trans_fact[trans['invoice-id']].append(key)

        for id_fact, par_fact in trans_fact.items():
            base = transactions.valeurs[par_fact[0]]
            id_classe = base['client-idclass']
            classe = imports.classes.donnees[id_classe]
            ref = classe['ref_fact'] + "_" + str(imports.edition.annee) + "_" + \
                Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(id_fact)
            total = 0
            for key in par_fact:
                trans = transactions.valeurs[key]
                total += trans['total-fact']

            ligne = []
            for cle in self.cles:
                if cle == 'invoice-ref':
                    ligne.append(ref)
                elif cle == 'total-fact':
                    ligne.append(round(2*total, 1)/2)
                else:
                    ligne.append(base[cle])
            self.lignes.append(ligne)
