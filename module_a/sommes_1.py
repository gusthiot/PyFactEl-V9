

class Sommes1(object):
    """
    Classe pour sommer les transactions 1
    """

    def __init__(self, transactions_1):
        """
        initialisation des données
        :param transactions_1: transactions 1 générées
        """
        self.par_fact = {'factures': {}, 'clients': {}}
        for key, trans in transactions_1.valeurs.items():
            factures = self.par_fact['factures']
            if trans['invoice-id'] not in factures:
                factures[trans['invoice-id']] = {'transactions': {'total': 0, 'keys': [key]},
                                                 'projets': {}}
            else:
                factures[trans['invoice-id']]['transactions']['keys'].append(key)
            factures[trans['invoice-id']]['transactions']['total'] += trans['total-fact']  # => bilan factures

            projets = factures[trans['invoice-id']]['projets']
            if trans['proj-id'] not in projets:
                projets[trans['proj-id']] = {}
            tp = projets[trans['proj-id']]
            if trans['item-order'] not in tp:
                tp[trans['item-order']] = {'keys': [key], 'id': trans['item-idsap'], 'total': 0}
            else:
                tp[trans['item-order']]['keys'].append(key)
            tp[trans['item-order']]['total'] += trans['total-fact']  # => factures
            articles = self.par_fact['clients']
            if trans['item-order'] not in articles:
                articles[trans['item-order']] = {'total': 0}
            articles[trans['item-order']]['total'] += trans['total-fact']  # => tickets
