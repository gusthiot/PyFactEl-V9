

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
                projets[trans['proj-id']] = {'items': {}, 'numero': trans['proj-nbr'],
                                             'intitule': trans['proj-name']}
            tpi = projets[trans['proj-id']]['items']
            if trans['item-order'] not in tpi:
                tpi[trans['item-order']] = {'keys': [], 'id': trans['item-idsap'], 'total': 0}
            tpi[trans['item-order']]['keys'].append(key)
            tpi[trans['item-order']]['total'] += trans['total-fact']
            # => factures

            if trans['client-code'] not in self.par_client:
                self.par_client[trans['client-code']] = {'articles': {}, 'factures': {}}
            factures = self.par_client[trans['client-code']]['factures']
            if trans['invoice-id'] not in factures:
                factures[trans['invoice-id']] = {'transactions': [], 'total': 0}
            factures[trans['invoice-id']]['transactions'].append(key)
            factures[trans['invoice-id']]['total'] += trans['total-fact']
            # => total

            articles = self.par_client[trans['client-code']]['articles']
            if trans['item-order'] not in articles:
                articles[trans['item-order']] = {'id': trans['item-idsap'], 'total': 0}
            articles[trans['item-order']]['total'] += trans['total-fact']
            # => tickets
