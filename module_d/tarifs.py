from core import (Outils,
                  CsvBase)


class Tarifs(CsvBase):
    """
    Classe pour la création du listing des tarifs
    """
    
    cles = ['invoice-year', 'invoice-month', 'item-id', 'client-idclass', 'valuation-price']

    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        super().__init__(imports.edition)
        self.nom = "tarif_" + str(imports.edition.annee) + "_" + Outils.mois_string(imports.edition.mois) + ".csv"

        for key in imports.categories.donnees.keys():
            cat = imports.categories.donnees[key]
            for id_classe in imports.classes.donnees.keys():
                unique = id_classe + cat['id_categorie']
                prix_unit = imports.categprix.donnees[unique]['prix_unit']
                donnee = [cat['id_categorie'], id_classe, prix_unit]
                self.ajouter_valeur(donnee, unique)

        for key in imports.prestations.donnees.keys():
            prest = imports.prestations.donnees[key]
            for id_classe in imports.classes.donnees.keys():
                coefprest = imports.coefprests.donnees[id_classe + prest['id_article']]
                prix_unit = round(prest['prix_unit'] * coefprest['coefficient'], 2)
                donnee = [prest['id_prestation'], id_classe, prix_unit]
                self.ajouter_valeur(donnee, id_classe + prest['id_prestation'])
