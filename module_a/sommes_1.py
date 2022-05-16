

class Sommes1(object):
    """
    Classe pour sommer les transactions 1
    """

    def __init__(self, transactions_1):
        """
        initialisation des données
        :param transactions_1: transactions 1 générées
        """
        self.par_fact = {}
        self.par_client = {}
        for key, trans in transactions_1.valeurs.items():
            if trans['invoice-id'] not in self.par_fact:
                self.par_fact[trans['invoice-id']] = {'transactions': {'total': 0, 'keys': []}, 'projets': {}}
            self.par_fact[trans['invoice-id']]['transactions']['keys'].append(key)
            self.par_fact[trans['invoice-id']]['transactions']['total'] += trans['total-fact']
            # => bilan factures

            projets = self.par_fact[trans['invoice-id']]['projets']
            if trans['proj-id'] not in projets:
                projets[trans['proj-id']] = {}
            tp = projets[trans['proj-id']]
            if trans['item-order'] not in tp:
                tp[trans['item-order']] = {'keys': [], 'id': trans['item-idsap'], 'total': 0}
            tp[trans['item-order']]['keys'].append(key)
            tp[trans['item-order']]['total'] += trans['total-fact']
            # => factures

            if trans['client-code'] not in self.par_client:
                self.par_client[trans['client-code']] = {}
            articles = self.par_client[trans['client-code']]
            if trans['item-order'] not in articles:
                articles[trans['item-order']] = {'id': trans['item-idsap'], 'total': 0}
            articles[trans['item-order']]['total'] += trans['total-fact']
            # => tickets
