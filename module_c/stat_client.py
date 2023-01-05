from core import (Format,
                  CsvList)


class StatClient(CsvList):
    """
    Classe pour la création du csv des stats nombre user
    """

    cles = ['year', 'month', 'client-code', 'client-sap', 'client-name', 'client-idclass',
            'client-class', 'client-labelclass', 'stat-trans', 'stat-run', 'stat-nbuser-m', 'stat-nbuser-3m',
            'stat-nbuser-6m', 'stat-nbuser-12m']

    def __init__(self, imports, par_ul, par_client):
        """
        initialisation des données
        :param imports: données importées
        :param par_ul: tri des users labo
        :param par_client: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Stat-client_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" \
                   + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        stats_clients = {}

        if imports.edition.annee in par_ul['annees'] and \
                imports.edition.mois in par_ul['annees'][imports.edition.annee]:
            pm = par_ul['annees'][imports.edition.annee][imports.edition.mois]['clients']
            for code in pm:
                stats_clients[code] = {'1m': len(pm[code]), '3m': pm[code].copy(), '6m': pm[code].copy(),
                                       '12m': pm[code].copy()}
        for gap in range(1, 12):
            if gap < imports.edition.mois:
                mo = imports.edition.mois - gap
                an = imports.edition.annee
            else:
                mo = 12 + imports.edition.mois - gap
                an = imports.edition.annee - 1
            if an in par_ul['annees']:
                if mo in par_ul['annees'][an]:
                    pm = par_ul['annees'][an][mo]['clients']
                    for code in pm:
                        if code not in stats_clients:
                            stats_clients[code] = {'1m': 0, '3m': [], '6m': [], '12m': []}
                        for idd in pm[code]:
                            if gap < 3 and idd not in stats_clients[code]['3m']:
                                stats_clients[code]['3m'].append(idd)
                            if gap < 6 and idd not in stats_clients[code]['6m']:
                                stats_clients[code]['6m'].append(idd)
                            if idd not in stats_clients[code]['12m']:
                                stats_clients[code]['12m'].append(idd)

        for code, stats in stats_clients.items():
            client = imports.clients.donnees[code]
            classe = imports.classes.donnees[client['id_classe']]
            nb = 0
            runs = 0
            if code in par_client.keys():
                nb = par_client[code]['nb']
                runs = par_client[code]['runs']

            self.lignes.append([imports.edition.annee, imports.edition.mois, client['code'], client['code_sap'],
                                client['abrev_labo'], client['id_classe'], classe['code_n'], classe['intitule'], nb,
                                runs, stats['1m'], len(stats['3m']), len(stats['6m']), len(stats['12m'])])
