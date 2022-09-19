from core import (Format,
                  CsvDict)
from imports.construits import Transactions2


class Journal(CsvDict):
    """
    Classe pour la création de la table des modifications des factures
    """

    def __init__(self, imports, versions, transactions_2):
        """
        initialisation des données
        :param imports: données importées
        :param versions: versions nouvellement générées
        :param transactions_2: transactions 2 générées
        """
        super().__init__(imports)
        self.nom = "Journal-corrections_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"
        self.cles = Transactions2.cles
        unique = 0

        for donnee in versions.corrections:
            if donnee[0] is not None:
                # print(imports.transactions_2.donnees[donnee[0]])
                self.valeurs[unique] = imports.transactions_2.donnees[donnee[0]]
            else:
                trans = transactions_2.valeurs[donnee[1]]
                version = str(int(trans['invoice-version'])-1)
                self._ajout_nul(trans, version, unique)
            unique += 1
            if donnee[1] is not None:
                # print(transactions_2.valeurs[donnee[1]])
                self.valeurs[unique] = transactions_2.valeurs[donnee[1]]
            else:
                trans = imports.transactions_2.donnees[donnee[0]]
                version = str(int(trans['invoice-version'])+1)
                self._ajout_nul(trans, version, unique)
            unique += 1

    def _ajout_nul(self, trans, version, unique):
        """
        ajout d'une ligne pour une transaction non-existante
        :param trans: transaction de l'autre version
        :param version: version de la transaction supposée
        :param unique: clé unique de la ligne
        """
        self._ajouter_valeur([trans['invoice-year'], trans['invoice-month'], version, trans['invoice-id'], "", "", "",
                              "", "", "", "", "", trans['proj-id'], "", "", trans['user-id'], "", "", "", "", "",
                              trans['item-idsap'], "", "", "", trans['item-id'], "", "", "", "", "", "", ""], unique)
