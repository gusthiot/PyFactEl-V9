from core import (Format,
                  CsvList,
                  Interface,
                  ErreurConsistance)
from imports.construits import Version


class VersionNew(CsvList):
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
        facts_new = {}
        for key, trans in self.transactions_new.items():
            if trans['invoice-id'] not in facts_new:
                facts_new[trans['invoice-id']] = []
            facts_new[trans['invoice-id']].append(key)

        if imports.version == 0:
            for fact_id, liste in facts_new.items():
                self.__add_new(fact_id, liste)
        else:
            self.transactions_old = imports.transactions_2.donnees
            facts_old = {}
            key = 0
            for trans in self.transactions_old:
                if trans['invoice-id'] not in facts_old:
                    facts_old[trans['invoice-id']] = []
                facts_old[trans['invoice-id']].append(key)
                key += 1
                if trans['invoice-year'] != imports.edition.annee:
                    Interface.fatal(ErreurConsistance(), "l'ancien transactions 2 se doit "
                                                         "d'être de la même année que le nouveau")
                if trans['invoice-month'] != imports.edition.mois:
                    Interface.fatal(ErreurConsistance(), "l'ancien transactions 2 se doit "
                                                         "d'être du même mois que le nouveau")
                if trans['invoice-version'] != imports.version-1:
                    Interface.fatal(ErreurConsistance(), "l'ancien transactions 2 se doit "
                                                         "d'être de la version du nouveau - 1")

            for fact_id, liste in facts_old.items():
                base_old = self.transactions_old[liste[0]]
                if fact_id not in imports.versions.donnees.keys():
                    Interface.fatal(ErreurConsistance(), "Un id-facture présent dans l'ancien transactions 2 se doit "
                                                         "d'être présent dans l'ancienne table des versions")
                old_v = imports.versions.donnees[fact_id]
                if old_v['client-code'] != base_old['client-code']:
                    Interface.fatal(ErreurConsistance(), "Le id-facture doit être lié au même client dans les anciennes"
                                                         " table des versions et transactions 2")

            for fact_id, donnee in imports.versions.donnees.items():
                if fact_id not in facts_new:
                    self.lignes.append([fact_id, donnee['client-code'], self.imports.version, 'CANCELED',
                                        donnee['version-new-amount'], 0])
                else:
                    liste_new = facts_new[fact_id]
                    base_new = self.transactions_new[liste_new[0]]
                    if donnee['client-code'] != base_new['client-code']:
                        Interface.fatal(ErreurConsistance(),
                                        "Le id-facture doit être lié au même client dans l'ancienne et "
                                        "la nouvelle table des versions")

                    liste_old = facts_old[fact_id]
                    struct_new = self.__struct_fact(transactions_2_new.valeurs, liste_new)
                    struct_old = self.__struct_fact(self.transactions_old, liste_old)
                    idem = True
                    if self.__compare(struct_new, struct_old, True, self.transactions_new, self.transactions_old):
                        idem = False
                    else:
                        if self.__compare(struct_old, struct_new):
                            idem = False

                    if idem:
                        self.lignes.append([fact_id, donnee['client-code'], donnee['version-last'], 'IDEM',
                                            donnee['version-new-amount'], donnee['version-new-amount']])
                    else:
                        somme = 0
                        for unique in liste_new:
                            trans = self.transactions_new[unique]
                            somme += trans['total-fact']
                        self.lignes.append([fact_id, donnee['client-code'], self.imports.version, 'CORRECTED',
                                            donnee['version-new-amount'], round(somme, 2)])

            for fact_id, liste in facts_new.items():
                if fact_id not in imports.versions.donnees.keys():
                    self.__add_new(fact_id, liste)

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
        self.lignes.append([fact_id, base['client-code'], self.imports.version, 'NEW', 0, round(somme, 2)])

    @staticmethod
    def __struct_fact(transactions, keys):
        """
        crée l'arborescence des transactions, fonction projet->articleSAP->article->utilisateur
        :param transactions: données transactions
        :param keys: liste des transactions concernées par la facture traitée
        :return: arborescence sous forme de dictionnaire
        """
        arbre = {}
        for key in keys:
            trans = transactions[key]
            if trans['proj-id'] not in arbre:
                arbre[trans['proj-id']] = {}
            tp = arbre[trans['proj-id']]
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
        for id_compte, par_compte in first.items():
            if id_compte not in second.keys():
                return True
            sec_compte = second[id_compte]
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
