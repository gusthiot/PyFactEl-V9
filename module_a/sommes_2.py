

class Sommes2(object):
    """
    Classe pour sommer les transactions 2
    """

    def __init__(self, transactions_2):
        """
        initialisation des données
        :param transactions_2: transactions 2 générées
        """
        self.par_fact = self.struct_fact(transactions_2.valeurs)

    @staticmethod
    def struct_fact(transactions):
        """
        crée l'arborescence des transactions, fonction projet->articleSAP->article->utilisateur
        :param transactions: données transactions
        :return: arborescence sous forme de dictionnaire
        """
        arbre = {}
        for key, trans in transactions.items():
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
