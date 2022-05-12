

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
        for key, trans in transactions_1.valeurs.items():
            if trans['invoice-id'] not in self.par_fact:
                self.par_fact[trans['invoice-id']] = {'transactions': [], 'projets': {}}
            self.par_fact[trans['invoice-id']]['transactions'].append(key)
            projets = self.par_fact[trans['invoice-id']]['projets']
            if trans['proj-id'] not in projets:
                projets[trans['proj-id']] = {}
            tp = projets[trans['proj-id']]
            if trans['item-idsap'] not in tp:
                tp[trans['item-idsap']] = [key]
            else:
                tp[trans['item-idsap']].append(key)
