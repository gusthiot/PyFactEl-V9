from core import (Format,
                  DossierDestination)


class Annexe(object):
    """
    Classe pour la création du csv d'annexe
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-id', 'platf-name', 'client-name', 'proj-nbr',
            'proj-name', 'user-name-f', 'date-start-y', 'date-start-m', 'date-end-y', 'date-end-m', 'item-labelcode',
            'item-name', 'transac-quantity', 'item-unit', 'valuation-price', 'deduct-CHF', 'total-fact']

    def __init__(self, imports, transactions, versions, csv_fichiers):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param versions: versions des factures générées
        :param csv_fichiers: fichiers csv et nom du fichier zip par client
        """

        pt = imports.paramtexte.donnees
        self.csv_fichiers = csv_fichiers

        for id_fact in versions.facts_new.keys():
            pf = versions.facts_new[id_fact]['transactions']
            base = transactions.valeurs[pf[0]]
            code = base['client-code']
            client = imports.clients.donnees[code]
            nom_zip = "Annexes_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + "_" + \
                      str(imports.version) + base['client-code'] + "_" + client['abrev_labo'] + ".zip"
            prefixe = "Annexe_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + \
                      "_" + str(imports.version)
            par_compte = {}
            for key in pf:
                id_compte = transactions.valeurs[key]['proj-id']
                if id_compte not in par_compte.keys():
                    par_compte[id_compte] = []
                par_compte[id_compte].append(key)
            lignes = []
            for id_compte, pc in par_compte.items():
                compte = imports.comptes.donnees[id_compte]
                nom_csv = prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_" + compte['numero'] + ".csv"
                if code not in self.csv_fichiers:
                    self.csv_fichiers[code] = {'nom': nom_zip, 'fichiers': []}
                self.csv_fichiers[code]['fichiers'].append(nom_csv)
                for key in pc:
                    trans = transactions.valeurs[key]
                    ligne = []
                    for cle in range(2, len(self.cles)):
                        ligne.append(trans[self.cles[cle]])
                    lignes.append(ligne)

                with DossierDestination(imports.chemin_cannexes).writer(nom_csv) as fichier_writer:
                    ligne = []
                    for cle in self.cles:
                        ligne.append(pt[cle])
                    fichier_writer.writerow(ligne)

                    for ligne in lignes:
                        fichier_writer.writerow(ligne)
