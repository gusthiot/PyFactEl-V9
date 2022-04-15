from core import (Outils,
                  CsvBase)


class Articles(CsvBase):
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
        self.nom = "article_" + str(imports.edition.annee) + "_" + Outils.mois_string(imports.edition.mois) + ".csv"

        for key in imports.categories.donnees.keys():
            cat = imports.categories.donnees[key]
            art = imports.artsap.donnees[cat['id_article']]
            donnee = [cat['id_categorie'], cat['no_categorie'], cat['intitule'], cat['unite'], cat['id_article'],
                      art['code_d'], art['flag_usage'], art['flag_conso'], art['eligible'], art['ordre'],
                      art['intitule'], cat['id_plateforme'], "FALSE"]
            self.ajouter_valeur(donnee, cat['id_categorie'])

        for key in imports.prestations.donnees.keys():
            prest = imports.prestations.donnees[key]
            art = imports.artsap.donnees[prest['id_article']]
            if prest['id_machine'] == "0":
                extra = "FALSE"
            else:
                extra = "TRUE"
            donnee = [prest['id_prestation'], prest['no_prestation'], prest['designation'],
                      prest['unite_prest'], prest['id_article'], art['code_d'], art['flag_usage'], art['flag_conso'],
                      art['eligible'], art['ordre'], art['intitule'], prest['id_plateforme'], extra]
            self.ajouter_valeur(donnee, prest['id_prestation'])
