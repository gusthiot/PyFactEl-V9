from core import (Format,
                  CsvDict)


class Modifications(CsvDict):
    """
    Classe pour la création de la table des modifications des factures
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'client-name', 'invoice-id', 'invoice-type',
            'version-change', 'version-old-amount', 'version-new-amount']

    def __init__(self, imports, versions):
        """
        initialisation des données
        :param imports: données importées
        :param versions: versions nouvellement générées
        """
        super().__init__(imports)
        self.nom = "Modif-factures_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for donnee in versions.valeurs.values():
            if donnee['version-change'] != 'IDEM':
                client = imports.clients.donnees[donnee['client-code']]
                self._ajouter_valeur([imports.edition.annee, imports.edition.mois, imports.version,
                                      client['abrev_labo'], donnee['invoice-id'], donnee['invoice-type'],
                                      donnee['version-change'], donnee['version-old-amount'],
                                      donnee['version-new-amount']], donnee['invoice-id'])
