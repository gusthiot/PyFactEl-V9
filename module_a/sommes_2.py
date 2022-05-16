

class Sommes2(object):
    """
    Classe pour sommer les transactions 2
    """

    def __init__(self, transactions_2):
        """
        initialisation des données
        :param transactions_2: transactions 2 générées
        """
        self.par_fact = {}
        for key, trans in transactions_2.valeurs.items():
            if trans['invoice-id'] not in self.par_fact:
                self.par_fact[trans['invoice-id']] = {'base': key, 'total': 0, 'projets': {}, 'comptes': {}}
            self.par_fact[trans['invoice-id']]['total'] += trans['total-fact']
            projets = self.par_fact[trans['invoice-id']]['projets']
            comptes = self.par_fact[trans['invoice-id']]['comptes']
            if trans['proj-id'] not in projets:
                projets[trans['proj-id']] = {}
            tp = projets[trans['proj-id']]
            if trans['item-idsap'] not in tp:
                tp[trans['item-idsap']] = {'items': {}, 'total': 0, 'base': key}
            tp[trans['item-idsap']]['total'] += trans['total-fact']
            # => transactions 1

            tps = tp[trans['item-idsap']]['items']
            if trans['item-id'] not in tps:
                tps[trans['item-id']] = {}
            tpsi = tps[trans['item-id']]
            if trans['user-id'] not in tpsi:
                tpsi[trans['user-id']] = []
            tpsi[trans['user-id']].append(key)
            # => versions / pdfs

            if trans['proj-id'] not in comptes.keys():
                comptes[trans['proj-id']] = []
            comptes[trans['proj-id']].append(key)
            # => annexes

    @staticmethod
    def sommes_old(transactions):
        """
        crée l'arborescence des anciennes transactions, fonction projet->articleSAP->article->utilisateur
        :param transactions: données transactions
        :return: arborescence sous forme de dictionnaire
        """
        arbre = {}
        for key, trans in transactions.items():
            if trans['invoice-id'] not in arbre:
                arbre[trans['invoice-id']] = {'projets': {}}
            projets = arbre[trans['invoice-id']]['projets']
            if trans['proj-id'] not in projets:
                projets[trans['proj-id']] = {}
            tp = projets[trans['proj-id']]
            if trans['item-idsap'] not in tp:
                tp[trans['item-idsap']] = {'items': {}}
            tps = tp[trans['item-idsap']]['items']
            if trans['item-id'] not in tps:
                tps[trans['item-id']] = {}
            tpsi = tps[trans['item-id']]
            if trans['user-id'] not in tpsi:
                tpsi[trans['user-id']] = []
            tpsi[trans['user-id']].append(key)
        return arbre
