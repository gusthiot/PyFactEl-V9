from core import (Interface,
                  Format,
                  DossierDestination)
from datetime import datetime
import calendar


class AnnexeSubsides(object):
    """
    Classe pour la création du csv d'annexe subsides
    """

    cles = ['proj-name', 'item-labelcode', 'subsid-name', 'subsid-start', 'subsid-end', 'subsid-pourcent',
            'subsid-maxproj', 'subsid-maxmois', 'subsid-alrdygrant', 'subsid-CHF', 'subsid-reste']

    def __init__(self, imports, par_client, csv_fichiers):
        """
        initialisation des données
        :param imports: données importées
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
            for id_compte in cc:
                compte = imports.comptes.donnees[id_compte]
                type_s = compte['type_subside']
                subside = imports.subsides.donnees[type_s]
                for id_article, artsap in imports.artsap.donnees.items():
                    plaf = type_s + imports.edition.plateforme + id_article
                    if plaf in imports.plafonds.donnees.keys():
                        plafond = imports.plafonds.donnees[plaf]
                        ligne = [compte['intitule'], artsap['intitule'], subside['intitule'], subside['debut'],
                                 subside['fin'], plafond['pourcentage'], plafond['max_compte'], plafond['max_mois']]
                        g_id = id_compte + imports.edition.plateforme + id_article
                        if g_id in imports.grants.donnees.keys():
                            grant, info = Format.est_un_nombre(imports.grants.donnees[g_id]['subsid-alrdygrant'],
                                                               "le montant de grant", mini=0, arrondi=2)
                            if info != "":
                                Interface.affiche_message(info)
                        else:
                            grant = 0
                        subs = 0
                        if code in par_client and id_compte in par_client[code]['comptes']:
                            par_code = par_client[code]['comptes'][id_compte]
                            if id_article in par_code.keys():
                                subs = par_code[id_article]['subs']

                        reste = plafond['max_compte'] - grant - subs
                        ligne += [round(grant, 2), round(subs, 2), round(reste, 2)]
                        lignes.append(ligne)

            if len(lignes) > 0:
                client = imports.clients.donnees[code]
                nom_csv = "Subsides_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                          Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + \
                          client['abrev_labo'] + ".csv"
                nom_zip = "Annexes_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                          Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + code + "_" + \
                          client['abrev_labo'] + ".zip"
                if code not in self.csv_fichiers:
                    self.csv_fichiers[code] = {'nom': nom_zip, 'fichiers': []}
                self.csv_fichiers[code]['fichiers'].append(nom_csv)
                with DossierDestination(imports.chemin_cannexes).writer(nom_csv) as fichier_writer:
                    ligne = []
                    for cle in self.cles:
                        ligne.append(pt[cle])
                    fichier_writer.writerow(ligne)

                    for ligne in lignes:
                        fichier_writer.writerow(ligne)
