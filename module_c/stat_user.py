from core import (Format,
                  CsvList)


class StatUser(CsvList):
    """
    Classe pour la création du csv des stats nombre user
    """

    cles = ['invoice-year', 'invoice-month', 'user-id', 'user-sciper', 'user-name', 'user-first', 'client-code',
            'client-sap', 'client-name', 'client-idclass', 'client-class', 'client-labelclass', 'stat-trans',
            'stat-run']

    def __init__(self, imports, transactions, par_user):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_user: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Stat-user_" + str(imports.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + "_" \
                   + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for par_client in par_user.values():
            for par_code in par_client.values():
                tbtr = par_code['transactions']
                ligne = [imports.edition.annee, imports.edition.mois]
                stat_trans = 0
                stat_run = 0
                base = transactions.valeurs[tbtr[0]]
                for cle in range(2, len(self.cles)-2):
                    ligne.append(base[self.cles[cle]])
                for indice in tbtr:
                    trans = transactions.valeurs[indice]
                    stat_trans += 1
                    if str(trans['transac-runcae']) == "1":
                        stat_run += 1
                ligne += [stat_trans, stat_run]
                self.lignes.append(ligne)
