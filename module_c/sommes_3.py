import datetime


class Sommes3(object):
    """
    Classe pour sommer les transactions 3 en fonction des clients et des plateformes
    """

    def __init__(self, imports, transactions_3):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        """
        self.par_client = {}
        self.par_item = {}
        self.par_user = {}
        self.par_machine = {}
        self.par_projet = {}

        for key, transaction in transactions_3.valeurs.items():
            code_client = transaction['client-code']
            id_compte = transaction['proj-id']
            user_id = transaction['user-id']

            # Module B : mois de traitement = mois de facturation
            if (imports.edition.annee == transaction['invoice-year'] and
                    imports.edition.mois == transaction['invoice-month']):
                if code_client not in self.par_client.keys():
                    self.par_client[code_client] = {'articles': {}, 'projets': {}, 'comptes': {}, 'nb': 0, 'runs': 0,
                                                    'val_2': 0, 'val_3': 0}

                if transaction['transac-valid'] == "2":
                    self.par_client[code_client]['val_2'] += transaction['valuation-net']
                if transaction['transac-valid'] == "3":
                    self.par_client[code_client]['val_3'] += transaction['valuation-net']
                # => bilan annulés

                id_compte_fact = transaction['invoice-project']
                pcp = self.par_client[code_client]['projets']
                if id_compte_fact not in pcp.keys():
                    pcp[id_compte_fact] = {'comptes': {}, 'transactions': []}

                pcp[id_compte_fact]['transactions'].append(key)
                # => annexe details

                nbr = transaction['item-nbr']
                order = transaction['item-order']
                if id_compte not in pcp[id_compte_fact]['comptes'].keys():
                    pcp[id_compte_fact]['comptes'][id_compte] = {}
                pcpc = pcp[id_compte_fact]['comptes'][id_compte]
                if order not in pcpc.keys():
                    pcpc[order] = {}
                pcpa = pcpc[order]
                if nbr not in pcpa.keys():
                    pcpa[nbr] = {}
                if user_id not in pcpa[nbr].keys():
                    pcpa[nbr][user_id] = {'base': key, 'quantity': 0, 'deduct': 0, 'total': 0,
                                          'start': transaction['transac-date'],
                                          'end': transaction['transac-date']}
                pcpa[nbr][user_id]['quantity'] += transaction['transac-quantity']
                pcpa[nbr][user_id]['deduct'] += transaction['deduct-CHF']
                pcpa[nbr][user_id]['total'] += transaction['total-fact']
                if transaction['transac-date'] < pcpa[nbr][user_id]['start']:
                    pcpa[nbr][user_id]['start'] = transaction['transac-date']
                if transaction['transac-date'] > pcpa[nbr][user_id]['end']:
                    pcpa[nbr][user_id]['end'] = transaction['transac-date']
                # => transactions 2

                id_article = transaction['item-idsap']
                pcc = self.par_client[code_client]['comptes']
                if id_compte not in pcc.keys():
                    pcc[id_compte] = {}
                pccd = pcc[id_compte]
                if id_article not in pccd.keys():
                    pccd[id_article] = {'subs': 0}
                if transaction['subsid-code'] != "" and transaction['subsid-maxproj'] > 0:
                    pccd[id_article]['subs'] += transaction['subsid-CHF']
                # => annexe subsides

                code_d = transaction['item-codeD']
                pca = self.par_client[code_client]['articles']
                if code_d not in pca.keys():
                    pca[code_d] = {'base': key, 'avant': 0, 'compris': 0, 'deduit': 0, 'sub_ded': 0, 'fact': 0,
                                   'remb': 0, 'sub_remb': 0}
                pca[code_d]['avant'] += transaction['valuation-brut']
                pca[code_d]['compris'] += transaction['valuation-net']
                pca[code_d]['deduit'] += transaction['deduct-CHF']
                pca[code_d]['sub_ded'] += transaction['subsid-deduct']
                pca[code_d]['fact'] += transaction['total-fact']
                pca[code_d]['remb'] += transaction['discount-bonus']
                pca[code_d]['sub_remb'] += transaction['subsid-bonus']
                # => bilan subsides

            # Module C : mois de traitement = mois d'activité
            if (imports.edition.annee == transaction['transac-date'].year and
                    imports.edition.mois == transaction['transac-date'].month):

                if code_client not in self.par_client.keys():
                    self.par_client[code_client] = {'articles': {}, 'projets': {}, 'comptes': {}, 'nb': 0, 'runs': 0,
                                                    'val_2': 0, 'val_3': 0}
                self.par_client[code_client]['nb'] += 1
                if str(transaction['transac-runcae']) == "1":
                    self.par_client[code_client]['runs'] += 1
                # => stat client

                item = transaction['item-id']
                if id_compte not in self.par_projet.keys():
                    self.par_projet[id_compte] = {}
                ppi = self.par_projet[id_compte]
                if item not in ppi.keys():
                    ppi[item] = {'base': key, 'goops': 0, 'extrops': 0, 'goint': 0, 'extrint': 0}
                net = transaction['valuation-net']

                if transaction['client-code'] == transaction['platf-code'] and transaction['transac-valid'] != "2":
                    if transaction['item-extra'] == "TRUE":
                        if transaction['proj-expl'] != "TRUE":
                            ppi[item]['extrint'] += net
                    else:
                        if transaction['proj-expl'] == "TRUE":
                            ppi[item]['goops'] += net
                        else:
                            ppi[item]['goint'] += net
                if transaction['item-extra'] == "TRUE":
                    if ((transaction['client-code'] == transaction['platf-code'] and transaction['proj-expl'] == "TRUE")
                            or transaction['transac-valid'] == "2"):
                        ppi[item]['goops'] += net
                # => bilan conso

                if item not in self.par_item.keys():
                    self.par_item[item] = {'base': key, 'usage': 0, 'runtime': 0, 'nn': 0, 'rts': []}
                self.par_item[item]['usage'] += transaction['transac-usage']
                if transaction['transac-runtime'] != "":
                    rti = transaction['transac-runtime']
                    self.par_item[item]['runtime'] += rti
                    self.par_item[item]['nn'] += 1
                    self.par_item[item]['rts'].append(rti)
                # => bilan usage

                id_machine = transaction['mach-id']
                if id_machine not in self.par_machine.keys():
                    self.par_machine[id_machine] = {}
                pmi = self.par_machine[id_machine]
                if item not in pmi.keys():
                    pmi[item] = {'base': key, 'quantity': 0, 'usage': 0, 'runtime': 0, 'nn': 0, 'rts': []}
                pmi[item]['quantity'] += transaction['transac-quantity']
                pmi[item]['usage'] += transaction['transac-usage']
                run = transaction['transac-runtime']
                if run != "":
                    pmi[item]['runtime'] += run
                    pmi[item]['nn'] += 1
                    pmi[item]['rts'].append(run)
                # => stat machine

                if user_id not in self.par_user.keys():
                    self.par_user[user_id] = {}
                if code_client not in self.par_user[user_id].keys():
                    self.par_user[user_id][code_client] = {'days': {}, 'base': key, 'stat_trans': 0, 'stat_run': 0}
                puc = self.par_user[user_id][code_client]
                puc['stat_trans'] += 1
                if str(transaction['transac-runcae']) == "1":
                    puc['stat_run'] += 1
                # => stat user

                day = transaction['transac-date'].day
                if day not in puc['days'].keys():
                    puc['days'][day] = key
                # => user labo
