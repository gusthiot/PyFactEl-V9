from core import Outils


class StatClient(object):
    """
    Classe pour la création du csv des stats nombre user
    """

    cles = ['invoice-year', 'invoice-month', 'client-code', 'client-sap', 'client-name', 'client-idclass',
            'client-class', 'client-labelclass', 'stat-trans', 'stat-run', 'stat-nbuser-m', 'stat-nbuser-3m',
            'stat-nbuser-6m', 'stat-nbuser-12m']

    def __init__(self, imports, transactions, par_ul, par_client):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_ul: tri des users labo
        :param par_client: tri des transactions
        """

        self.imports = imports
        self.plateforme = imports.plateformes.donnees[imports.edition.plateforme]

        self.nom = "Stat-client_" + str(self.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + "_" \
                   + Outils.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        stats_clients = {}

        if imports.edition.mois in par_ul['annees'][imports.edition.annee]:
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

        self.lignes = []
        plate_name = ""
        for code in par_client.keys():
            tbtr = par_client[code]['transactions']
            base = transactions.valeurs[tbtr[0]]
            if plate_name == "":
                plate_name = base['platf-name']
            ligne = [imports.edition.annee, imports.edition.mois]
            for cle in range(2, len(self.cles)-6):
                ligne.append(base[self.cles[cle]])
            stat_run = 0
            for indice in tbtr:
                if str(transactions.valeurs[indice]['transac-runcae']) == "1":
                    stat_run += 1
            stats = stats_clients[code]
            ligne += [len(tbtr), stat_run, stats['1m'], len(stats['3m']), len(stats['6m']), len(stats['12m'])]
            self.lignes.append(ligne)

    def csv(self, dossier_destination):
        """
        création du fichier csv à partir de la liste des noms de colonnes
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """

        pt = self.imports.paramtexte.donnees

        with dossier_destination.writer(self.nom) as fichier_writer:
            ligne = []
            for cle in self.cles:
                ligne.append(pt[cle])
            fichier_writer.writerow(ligne)

            for ligne in self.lignes:
                fichier_writer.writerow(ligne)
