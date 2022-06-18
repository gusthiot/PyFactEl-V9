from core import (Format,
                  CsvList)


class BilanAnnules(CsvList):
    """
    Classe pour la création du csv de bilan annulés
    """

    cles = ['invoice-year', 'invoice-month', 'client-code', 'client-name', 'valuation-net-cancel',
            'valuation-net-notbill']

    def __init__(self, imports, par_client):
        """
        initialisation des données
        :param imports: données importées
        :param par_client: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Bilan-annulé_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for code, par_code in par_client.items():
            client = imports.clients.donnees[code]
            if par_code['val_2'] > 0 or par_code['val_3'] > 0:
                self.lignes.append([imports.edition.annee, imports.edition.mois, client['code'], client['abrev_labo'],
                                    par_code['val_2'], par_code['val_3']])
