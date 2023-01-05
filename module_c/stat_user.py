from core import (Format,
                  CsvList)


class StatUser(CsvList):
    """
    Classe pour la création du csv des stats nombre user
    """

    cles = ['year', 'month', 'user-id', 'user-sciper', 'user-name', 'user-first', 'client-code',
            'client-sap', 'client-name', 'client-idclass', 'client-class', 'client-labelclass', 'stat-trans',
            'stat-run']

    def __init__(self, imports, transactions_3, par_user):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_user: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Stat-user_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" \
                   + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for par_client in par_user.values():
            for par_code in par_client.values():
                ligne = [imports.edition.annee, imports.edition.mois]
                base = transactions_3.valeurs[par_code['base']]
                for cle in range(2, len(self.cles)-2):
                    ligne.append(base[self.cles[cle]])
                ligne += [par_code['stat_trans'], par_code['stat_run']]
                self.lignes.append(ligne)
