from core import (Format,
                  CsvDict,
                  Interface,
                  ErreurConsistance)
from imports.construits import Version
from module_a import Sommes2


class VersionNew(CsvDict):
    """
    Classe pour la création de la table des numéros de facture
    """

    def __init__(self, imports, transactions_2_new, sommes_2):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_2_new: transactions 2 nouvellement générées
        :param sommes_2: sommes des transactions 2
        """
        super().__init__(imports)
        self.nom = "Table-versions-factures_" + str(imports.edition.annee) + "_" + \
                   Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"
        self.cles = Version.cles

        self.transactions_new = transactions_2_new.valeurs

        self.corrections = []

        if imports.version == 0:
            for fact_id in sommes_2.par_fact.keys():
                self.__add_new(fact_id, sommes_2.par_fact[fact_id])
        else:
            transactions_old = imports.transactions_2.donnees
            sommes_2_old = Sommes2.sommes_old(transactions_old)

            for fact_id, donnee in imports.versions.donnees.items():
                if fact_id not in sommes_2.par_fact.keys():
                    if fact_id in sommes_2_old.keys():
                        self._ajouter_valeur([fact_id, donnee['client-code'], donnee['invoice-type'],
                                              self.imports.version, 'CANCELED', donnee['version-new-amount'], 0],
                                             fact_id)
                    else:
                        self._ajouter_valeur([fact_id, donnee['client-code'], donnee['invoice-type'],
                                              donnee['version-last'], 'IDEM', donnee['version-new-amount'],
                                              donnee['version-new-amount']], fact_id)

                else:
                    base_new = self.transactions_new[sommes_2.par_fact[fact_id]['base']]
                    if donnee['client-code'] != base_new['client-code']:
                        Interface.fatal(ErreurConsistance(),
                                        str(fact_id) + "\n Le id-facture doit être lié au même client dans l'ancienne"
                                        " et la nouvelle table des versions")
                    if donnee['invoice-type'] != base_new['invoice-type']:
                        Interface.fatal(ErreurConsistance(),
                                        str(fact_id) + "\n Le type de facture doit être le même dans l'ancienne et "
                                        "la nouvelle table des versions")

                    idem = True
                    if self.__compare(sommes_2.par_fact[fact_id], sommes_2_old[fact_id], True,
                                      self.transactions_new, transactions_old):
                        idem = False
                    if self.__compare(sommes_2_old[fact_id], sommes_2.par_fact[fact_id]):
                        idem = False

                    if idem:
                        self._ajouter_valeur([fact_id, donnee['client-code'], donnee['invoice-type'],
                                              donnee['version-last'], 'IDEM', donnee['version-new-amount'],
                                              donnee['version-new-amount']], fact_id)
                    else:
                        self._ajouter_valeur([fact_id, donnee['client-code'], donnee['invoice-type'],
                                              self.imports.version, 'CORRECTED', donnee['version-new-amount'],
                                              round(sommes_2.par_fact[fact_id]['total'], 2)], fact_id)

            for fact_id in sommes_2.par_fact.keys():
                if fact_id not in imports.versions.donnees.keys():
                    self.__add_new(fact_id, sommes_2.par_fact[fact_id])

    def __add_new(self, fact_id, somme_fact):
        """
        ajout d'une nouvelle facture aux versions
        :param fact_id: id de facture
        :param somme_fact: partie de la somme concernant la facture spécifiée
        """
        base = self.transactions_new[somme_fact['base']]
        self._ajouter_valeur([fact_id, base['client-code'], base['invoice-type'], self.imports.version, 'NEW', 0,
                              round(somme_fact['total'], 2)], fact_id)

    def __ajout_correction(self, par_user, sens):
        """
        ajout d'une correction au journal, dans le cas où une des transaction n'existe pas
        :param par_user: transaction(s) existante(s) pour un utilisateur (normalement une seule)
        :param sens: si nouvelle ou ancienne transaction
        """
        if len(par_user) > 1:
            Interface.fatal(ErreurConsistance(),
                            "Peut-on avoir plus d'une entrée par feuille d'arborescence ?")
        if sens:
            self.corrections.append([None, par_user[0]])
        else:
            self.corrections.append([par_user[0], None])

    def __compare(self, first, second, comparaison_fine=False, fdata=None, sdata=None):
        """
        compare les arborescences d'une facture entre 2 jeux de transactions
        :param first: clés du premier jeu
        :param second: clés du second jeu
        :param comparaison_fine: pour comparer les données en plus de l'arborescence (nouvelles données en premier)
        :param fdata: données du premier jeu
        :param sdata: données du second jeu
        :return: True s'il y a une différence, False autrement
        """
        diff = False
        for id_compte, par_compte in first['projets'].items():
            if id_compte not in second['projets'].keys():
                diff = True
                for id_article, par_article in par_compte['articles'].items():
                    for id_item, par_item in par_article['items'].items():
                        for id_user, par_user in par_item.items():
                            self.__ajout_correction(par_user, comparaison_fine)
            else:
                sec_compte = second['projets'][id_compte]['articles']
                for id_article, par_article in par_compte['articles'].items():
                    if id_article not in sec_compte.keys():
                        diff = True
                        for id_item, par_item in par_article['items'].items():
                            for id_user, par_user in par_item.items():
                                self.__ajout_correction(par_user, comparaison_fine)
                    else:
                        sec_article = sec_compte[id_article]
                        for id_item, par_item in par_article['items'].items():
                            if id_item not in sec_article['items'].keys():
                                diff = True
                                for id_user, par_user in par_item.items():
                                    self.__ajout_correction(par_user, comparaison_fine)
                            else:
                                sec_item = sec_article['items'][id_item]
                                for id_user, par_user in par_item.items():
                                    if id_user not in sec_item.keys():
                                        diff = True
                                        self.__ajout_correction(par_user, comparaison_fine)
                                    else:
                                        if comparaison_fine:
                                            sec_user = sec_item[id_user]
                                            if len(par_user) > 1 or len(sec_user) > 1:
                                                Interface.fatal(ErreurConsistance(),
                                                                "Peut-on avoir plus d'une entrée par "
                                                                "feuille d'arborescence ?")
                                            fd = fdata[par_user[0]]
                                            sd = sdata[sec_user[0]]
                                            if (sd['proj-nbr'] != fd['proj-nbr'] or
                                                    sd['proj-name'] != fd['proj-name'] or
                                                    sd['user-name-f'] != fd['user-name-f'] or
                                                    sd['date-start-y'] != fd['date-start-y'] or
                                                    sd['date-start-m'] != fd['date-start-m'] or
                                                    sd['date-end-y'] != fd['date-end-y'] or
                                                    sd['date-end-m'] != fd['date-end-m'] or
                                                    sd['total-fact'] != fd['total-fact']):
                                                diff = True
                                                self.corrections.append([sec_user[0], par_user[0]])
        return diff
