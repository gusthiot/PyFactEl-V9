from core import (Interface,
                  Format,
                  DossierDestination)
from datetime import datetime
import calendar


class AnnexeSubsides(object):
    """
    Classe pour la création du csv d'annexe subsides
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'platf-name', 'client-code', 'client-name', 'proj-id',
            'proj-name', 'item-codeD', 'item-labelcode', 'subsid-code', 'subsid-name', 'subsid-start', 'subsid-end',
            'subsid-pourcent', 'subsid-maxproj', 'subsid-maxmois', 'subsid-alrdygrant', 'subsid-CHF', 'subsid-reste']

    def __init__(self, imports, transactions, par_client, csv_fichiers):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_client: tri des transactions
        :param csv_fichiers: fichiers csv et nom du fichier zip par client
        """

        pt = imports.paramtexte.donnees
        self.csv_fichiers = csv_fichiers

        clients_comptes = {}
        for id_compte, compte in imports.comptes.donnees.items():
            type_s = compte['type_subside']
            if type_s != "":
                if type_s in imports.subsides.donnees.keys():
                    subside = imports.subsides.donnees[type_s]
                    if subside['debut'] != 'NULL':
                        debut, info = Format.est_une_date(subside['debut'], "la date de début")
                        if info != "":
                            Interface.affiche_message(info)
                    else:
                        debut = 'NULL'
                    if subside['fin'] != 'NULL':
                        fin, info = Format.est_une_date(subside['fin'], "la date de fin")
                        if info != "":
                            Interface.affiche_message(info)
                    else:
                        fin = 'NULL'

                    premier, dernier = calendar.monthrange(imports.edition.annee, imports.edition.mois)
                    if debut == "NULL" or debut <= datetime(imports.edition.annee, imports.edition.mois, dernier):
                        if fin == "NULL" or fin >= datetime(imports.edition.annee, imports.edition.mois, 1):
                            code_client = compte['code_client']
                            if code_client not in clients_comptes:
                                clients_comptes[code_client] = []
                            clients_comptes[code_client].append(id_compte)

        for code, cc in clients_comptes.items():
            lignes = []
            client = imports.clients.donnees[code]
            nom_csv = "Subsides_bilan_" + str(imports.edition.annee) + "_" + \
                      Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + \
                      client['abrev_labo'] + ".csv"
            nom_zip = "Annexes_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + "_" + \
                      str(imports.version) + "_" + code + "_" + client['abrev_labo'] + ".zip"
            if code not in self.csv_fichiers:
                self.csv_fichiers[code] = {'nom': nom_zip, 'fichiers': []}
            self.csv_fichiers[code]['fichiers'].append(nom_csv)
            for id_compte in cc:
                compte = imports.comptes.donnees[id_compte]
                type_s = compte['type_subside']
                subside = imports.subsides.donnees[type_s]

                for id_article, artsap in imports.artsap.donnees.items():
                    plaf = type_s + imports.plateforme['id_plateforme'] + id_article
                    if plaf in imports.plafonds.donnees.keys():
                        plafond = imports.plafonds.donnees[plaf]
                        ligne = [imports.edition.annee, imports.edition.mois, imports.version,
                                 imports.plateforme['abrev_plat'], client['code'], client['abrev_labo'],
                                 compte['id_compte'], compte['intitule'], id_article,
                                 artsap['intitule'], subside['type'], subside['intitule'], subside['debut'],
                                 subside['fin'], plafond['pourcentage'], plafond['max_compte'], plafond['max_mois']]
                        subs = 0
                        g_id = id_compte + imports.plateforme['id_plateforme'] + id_article
                        if g_id in imports.grants.donnees.keys():
                            grant, info = Format.est_un_nombre(imports.grants.donnees[g_id]['subsid-alrdygrant'],
                                                               "le montant de grant", mini=0, arrondi=2)
                            if info != "":
                                Interface.affiche_message(info)
                        else:
                            grant = 0
                        if code in par_client and id_compte in par_client[code]['comptes']:
                            par_code = par_client[code]['comptes'][id_compte]
                            if id_article in par_code.keys():
                                tbtr = par_code[id_article]
                                for indice in tbtr:
                                    trans = transactions.valeurs[indice]
                                    if trans['subsid-code'] != "" and trans['subsid-maxproj'] > 0:
                                        subs += trans['subsid-CHF']

                        reste = plafond['max_compte'] - grant - subs
                        ligne += [round(grant, 2), round(subs, 2), round(reste, 2)]
                        lignes.append(ligne)

            with DossierDestination(imports.chemin_cannexes).writer(nom_csv) as fichier_writer:
                ligne = []
                for cle in self.cles:
                    ligne.append(pt[cle])
                fichier_writer.writerow(ligne)

                for ligne in lignes:
                    fichier_writer.writerow(ligne)
