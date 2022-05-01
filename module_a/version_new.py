from core import (Format,
                  CsvDict,
                  Interface,
                  ErreurConsistance)
from imports.construits import Version


class VersionNew(CsvDict):
    """
    Classe pour la création de la table des numéros de facture
    """

    def __init__(self, imports, transactions_2_new):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_2_new: transactions 2 nouvellement générées
        """
        super().__init__(imports)
        self.nom = "Table-versions-factures_" + str(imports.edition.annee) + "_" + \
                   Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"
        self.cles = Version.cles

        self.transactions_new = transactions_2_new.valeurs
        self.facts_new = self.__struct_fact(self.transactions_new, "Nouveau Transitions 2 : ", self.imports.version)

        if imports.version == 0:
            for fact_id in self.facts_new.keys():
                self.__add_new(fact_id, self.facts_new[fact_id]['transactions'])
        else:
            transactions_old = imports.transactions_2.donnees
            facts_old = self.__struct_fact(transactions_old, "Ancien Transitions 2 : ", self.imports.version-1)

            for fact_id, donnee in imports.versions.donnees.items():
                if fact_id not in self.facts_new:
                    self._ajouter_valeur([fact_id, donnee['client-code'], self.imports.version, 'CANCELED',
                                          donnee['version-new-amount'], 0], fact_id)
                else:
                    base_new = self.transactions_new[self.facts_new[fact_id]['transactions'][0]]
                    if donnee['client-code'] != base_new['client-code']:
                        Interface.fatal(ErreurConsistance(),
                                        "Le id-facture doit être lié au même client dans l'ancienne et "
                                        "la nouvelle table des versions")

                    idem = True
                    if self.__compare(self.facts_new[fact_id], facts_old[fact_id], True, self.transactions_new,
                                      transactions_old):
                        idem = False
                    else:
                        if self.__compare(facts_old[fact_id], self.facts_new[fact_id]):
                            idem = False

                    if idem:
                        self._ajouter_valeur([fact_id, donnee['client-code'], donnee['version-last'], 'IDEM',
                                              donnee['version-new-amount'], donnee['version-new-amount']], fact_id)
                    else:
                        somme = 0
                        for unique in self.facts_new[fact_id]['transactions']:
                            trans = self.transactions_new[unique]
                            somme += trans['total-fact']
                        self._ajouter_valeur([fact_id, donnee['client-code'], self.imports.version, 'CORRECTED',
                                              donnee['version-new-amount'], round(somme, 2)], fact_id)

            for fact_id in self.facts_new.keys():
                if fact_id not in imports.versions.donnees.keys():
                    self.__add_new(fact_id, self.facts_new[fact_id]['transactions'])

    def __add_new(self, fact_id, liste):
        """
        ajout d'une nouvelle facture aux versions
        :param fact_id: id de facture
        :param liste: liste des transactions concernées par cette facture
        """
        somme = 0
        base = self.transactions_new[liste[0]]
        for unique in liste:
            trans = self.transactions_new[unique]
            somme += trans['total-fact']
        self._ajouter_valeur([fact_id, base['client-code'], self.imports.version, 'NEW', 0, round(somme, 2)], fact_id)

    def __struct_fact(self, transactions, label, version):
        """
        crée l'arborescence des transactions, fonction projet->articleSAP->article->utilisateur
        :param transactions: données transactions
        :return: arborescence sous forme de dictionnaire
        """
        arbre = {}
        for key, trans in transactions.items():
            if trans['invoice-year'] != self.imports.edition.annee:
                Interface.fatal(ErreurConsistance(), label + " mauvaise année à la ligne " + key)
            if trans['invoice-month'] != self.imports.edition.mois:
                Interface.fatal(ErreurConsistance(), label + " mauvais mois à la ligne " + key)
            if trans['invoice-version'] != version:
                Interface.fatal(ErreurConsistance(), label + " mauvaise version à la ligne " + key)
            if trans['invoice-id'] not in arbre:
                arbre[trans['invoice-id']] = {'transactions': [], 'projets': {}}
            arbre[trans['invoice-id']]['transactions'].append(key)
            projets = arbre[trans['invoice-id']]['projets']
            if trans['proj-id'] not in projets:
                projets[trans['proj-id']] = {}
            tp = projets[trans['proj-id']]
            if trans['item-idsap'] not in tp:
                tp[trans['item-idsap']] = {}
            tps = tp[trans['item-idsap']]
            if trans['item-id'] not in tps:
                tps[trans['item-id']] = {}
            tpsi = tps[trans['item-id']]
            if trans['user-id'] not in tpsi:
                tpsi[trans['user-id']] = [key]
            else:
                tpsi[trans['user-id']].append(key)
        return arbre

    @staticmethod
    def __compare(first, second, comparaison_fine=False, fdata=None, sdata=None):
        """
        compare les arborescences d'une facture entre 2 jeux de transactions
        :param first: clés du premier jeu
        :param second: clés du second jeu
        :param comparaison_fine: si on veut comparer les données en plus de l'arborescence
        :param fdata: données du premier jeu
        :param sdata: données du second jeu
        :return: True s'il y a une différence, False autrement
        """
        for id_compte, par_compte in first['projets'].items():
            if id_compte not in second['projets'].keys():
                return True
            sec_compte = second['projets'][id_compte]
            for id_article, par_article in par_compte.items():
                if id_article not in sec_compte.keys():
                    return True
                sec_article = sec_compte[id_article]
                for id_item, par_item in par_article.items():
                    if id_item not in sec_article.keys():
                        return True
                    sec_item = sec_article[id_item]
                    for id_user, par_user in par_item.items():
                        if id_user not in sec_item.keys():
                            return True
                        if comparaison_fine:
                            sec_user = sec_item[id_user]
                            if len(par_user) > 1 or len(sec_user) > 1:
                                Interface.fatal(ErreurConsistance(),
                                                "Peut-on avoir plus d'une entrée par feuille d'arborescence ?")
                            fd = fdata[par_user[0]]
                            sd = sdata[sec_user[0]]
                            if sd['proj-nbr'] != fd['proj-nbr']:
                                print('proj-nbr')
                                return True
                            if sd['proj-name'] != fd['proj-name']:
                                print('proj-name')
                                return True
                            if sd['user-name-f'] != fd['user-name-f']:
                                print('user-name-f')
                                return True
                            if sd['date-start-y'] != fd['date-start-y']:
                                print('date-start-y')
                                return True
                            if sd['date-start-m'] != fd['date-start-m']:
                                print('date-start-m')
                                return True
                            if sd['date-end-y'] != fd['date-end-y']:
                                print('date-end-y')
                                return True
                            if sd['date-end-m'] != fd['date-end-m']:
                                print('date-end-m')
                                return True
                            if sd['total-fact'] != fd['total-fact']:
                                print('total-fact')
                                return True
        return False
