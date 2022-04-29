

class Sommes(object):
    """
    Classe pour sommer les transactions en fonction des clients et des plateformes
    """

    def __init__(self, imports, transactions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        """
        self.par_client = {}
        self.par_item = {}
        self.par_user = {}
        self.par_machine = {}
        self.par_projet = {}

        for key, transaction in transactions.valeurs.items():
            code_client = transaction['client-code']
            id_compte = transaction['proj-id']
            user_id = transaction['user-id']

            # Module B : mois de traitement = mois de facturation
            if (imports.edition.annee == transaction['invoice-year'] and
                    imports.edition.mois == transaction['invoice-month']):
                if code_client not in self.par_client.keys():
                    self.par_client[code_client] = {'articles': {}, 'projets': {}, 'comptes': {}, 'transactions': []}

                id_compte_fact = transaction['invoice-project']
                pcp = self.par_client[code_client]['projets']
                if id_compte_fact not in pcp.keys():
                    pcp[id_compte_fact] = {'articles': {}, 'transactions': []}

                pcp[id_compte_fact]['transactions'].append(key)  # => annexe details

                nbr = transaction['item-nbr']
                order = transaction['item-order']
                if order not in pcp[id_compte_fact]['articles'].keys():
                    pcp[id_compte_fact]['articles'][order] = {}
                pcpa = pcp[id_compte_fact]['articles'][order]
                if nbr not in pcpa.keys():
                    pcpa[nbr] = {}
                if user_id not in pcpa[nbr].keys():
                    pcpa[nbr][user_id] = [key]
                else:
                    pcpa[nbr][user_id].append(key)  # => transactions 2

                id_article = transaction['item-idsap']
                pcc = self.par_client[code_client]['comptes']
                if id_compte not in pcc.keys():
                    pcc[id_compte] = {}
                pccd = pcc[id_compte]
                if id_article not in pccd.keys():
                    pccd[id_article] = [key]
                else:
                    pccd[id_article].append(key)  # => annexe subsides

                code_d = transaction['item-codeD']
                pca = self.par_client[code_client]['articles']
                if code_d not in pca.keys():
                    pca[code_d] = [key]
                else:
                    pca[code_d].append(key)  # => bilan subsides

            # Module C : mois de traitement = mois d'activité
            if (imports.edition.annee == transaction['transac-date'].year and
                    imports.edition.mois == transaction['transac-date'].month):

                if code_client not in self.par_client.keys():
                    self.par_client[code_client] = {'articles': {}, 'projets': {}, 'comptes': {}, 'transactions': []}

                self.par_client[code_client]['transactions'].append(key)  # => stat client

                item = transaction['item-id']
                if id_compte not in self.par_projet.keys():
                    self.par_projet[id_compte] = {}
                ppi = self.par_projet[id_compte]
                if item not in ppi.keys():
                    ppi[item] = [key]
                else:
                    ppi[item].append(key)  # => bilan conso

                if item not in self.par_item.keys():
                    self.par_item[item] = [key]
                else:
                    self.par_item[item].append(key)  # => bilan usage

                id_machine = transaction['mach-id']
                if id_machine not in self.par_machine.keys():
                    self.par_machine[id_machine] = {}
                pmi = self.par_machine[id_machine]
                if item not in pmi.keys():
                    pmi[item] = [key]
                else:
                    pmi[item].append(key)  # => stat machine

                if user_id not in self.par_user.keys():
                    self.par_user[user_id] = {}
                if code_client not in self.par_user[user_id].keys():
                    self.par_user[user_id][code_client] = {'days': {}, 'transactions': []}
                puc = self.par_user[user_id][code_client]
                puc['transactions'].append(key)  # => stat user
                day = transaction['transac-date'].day
                if day not in puc['days'].keys():
                    puc['days'][day] = key  # => user labo
