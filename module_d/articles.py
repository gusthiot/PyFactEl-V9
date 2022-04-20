from core import (Format,
                  CsvDict)


class Articles(CsvDict):
    """
    Classe pour la création du listing des articles
    """

    cles = ['invoice-year', 'invoice-month', 'item-id', 'item-nbr', 'item-name', 'item-unit', 'item-idsap',
            'item-codeD', 'item-flag-usage', 'item-flag-conso', 'item-eligible', 'item-order', 'item-labelcode',
            'platf-code', 'item-extra']

    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        super().__init__(imports)
        self.nom = "article_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + ".csv"

        for cat in imports.categories.donnees.values():
            art = imports.artsap.donnees[cat['id_article']]
            donnee = [self.imports.edition.annee, self.imports.edition.mois, cat['id_categorie'], cat['no_categorie'],
                      cat['intitule'], cat['unite'], cat['id_article'], art['code_d'], art['flag_usage'],
                      art['flag_conso'], art['eligible'], art['ordre'], art['intitule'], cat['id_plateforme'], "FALSE"]
            self._ajouter_valeur(donnee, cat['id_categorie'])

        for prest in imports.prestations.donnees.values():
            art = imports.artsap.donnees[prest['id_article']]
            if prest['id_machine'] == "0":
                extra = "FALSE"
            else:
                extra = "TRUE"
            donnee = [self.imports.edition.annee, self.imports.edition.mois, prest['id_prestation'],
                      prest['no_prestation'], prest['designation'], prest['unite_prest'], prest['id_article'],
                      art['code_d'], art['flag_usage'], art['flag_conso'], art['eligible'], art['ordre'],
                      art['intitule'], prest['id_plateforme'], extra]
            self._ajouter_valeur(donnee, prest['id_prestation'])
