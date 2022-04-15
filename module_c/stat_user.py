from core import Outils


class StatUser(object):
    """
    Classe pour la création du csv des stats nombre user
    """

    cles = ['invoice-year', 'invoice-month', 'user-id', 'user-sciper', 'user-name', 'user-first', 'client-code',
            'client-sap', 'client-name', 'client-idclass', 'client-class', 'client-labelclass', 'stat-trans',
            'stat-run']

    def __init__(self, imports, transactions, par_user):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_user: tri des transactions
        """

        self.imports = imports
        self.plateforme = imports.plateformes.donnees[imports.edition.plateforme]

        self.nom = "Stat-user_" + str(self.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + "_" \
                   + Outils.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        self.lignes = []
        for id_user in par_user.keys():
            par_client = par_user[id_user]
            for code in par_client.keys():
                tbtr = par_client[code]['transactions']
                ligne = [imports.edition.annee, imports.edition.mois]
                stat_trans = 0
                stat_run = 0
                base = transactions.valeurs[tbtr[0]]
                for cle in range(2, len(self.cles)-2):
                    ligne.append(base[self.cles[cle]])
                for indice in tbtr:
                    trans = transactions.valeurs[indice]
                    stat_trans += 1
                    if str(trans['transac-runcae']) == "1":
                        stat_run += 1
                ligne += [stat_trans, stat_run]
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
