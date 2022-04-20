from core import (Format,
                  CsvDict)


class Tarifs(CsvDict):
    """
    Classe pour la création du listing des tarifs
    """
    
    cles = ['invoice-year', 'invoice-month', 'item-id', 'client-idclass', 'valuation-price']

    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        super().__init__(imports)
        self.nom = "tarif_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + ".csv"

        for cat in imports.categories.donnees.values():
            for id_classe in imports.classes.donnees.keys():
                unique = id_classe + cat['id_categorie']
                prix_unit = imports.categprix.donnees[unique]['prix_unit']
                donnee = [self.imports.edition.annee, self.imports.edition.mois, cat['id_categorie'], id_classe,
                          prix_unit]
                self._ajouter_valeur(donnee, unique)

        for prest in imports.prestations.donnees.values():
            for id_classe in imports.classes.donnees.keys():
                coefprest = imports.coefprests.donnees[id_classe + prest['id_article']]
                prix_unit = round(prest['prix_unit'] * coefprest['coefficient'], 2)
                donnee = [self.imports.edition.annee, self.imports.edition.mois, prest['id_prestation'], id_classe,
                          prix_unit]
                self._ajouter_valeur(donnee, id_classe + prest['id_prestation'])
