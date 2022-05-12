from core import (Format,
                  DossierDestination)


class Annexe(object):
    """
    Classe pour la création du csv d'annexe
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-id', 'platf-name', 'client-name', 'proj-nbr',
            'proj-name', 'user-name-f', 'date-start-y', 'date-start-m', 'date-end-y', 'date-end-m', 'item-labelcode',
            'item-name', 'transac-quantity', 'item-unit', 'valuation-price', 'deduct-CHF', 'total-fact']

    def __init__(self, imports, transactions_2, sommes_2, csv_fichiers):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_2: transactions 2 générées
        :param sommes_2: sommes des transactions 2
        :param csv_fichiers: fichiers csv et nom du fichier zip par client
        """

        pt = imports.paramtexte.donnees
        self.csv_fichiers = csv_fichiers

        for id_fact in sommes_2.par_fact.keys():
            pf = sommes_2.par_fact[id_fact]['transactions']
            base = transactions_2.valeurs[pf[0]]
            code = base['client-code']
            intype = base['invoice-type']
            client = imports.clients.donnees[code]
            nom_zip = "Annexes_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + "_" + \
                      str(imports.version) + "_" + base['client-code'] + "_" + client['abrev_labo'] + ".zip"
            prefixe = "Annexe_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + \
                      "_" + str(imports.version)

            lignes = []
            par_compte = {}
            for key in pf:
                id_compte = transactions_2.valeurs[key]['proj-id']
                if id_compte not in par_compte.keys():
                    par_compte[id_compte] = []
                par_compte[id_compte].append(key)

            if intype == "GLOB":
                nom_csv = prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_0.csv"
            else:
                compte = imports.comptes.donnees[base['proj-id']]
                nom_csv = prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_" + compte['numero'] + ".csv"

            if code not in self.csv_fichiers:
                self.csv_fichiers[code] = {'nom': nom_zip, 'fichiers': []}
            self.csv_fichiers[code]['fichiers'].append(nom_csv)

            for pc in par_compte.values():
                for key in pc:
                    trans = transactions_2.valeurs[key]
                    ligne = []
                    for cle in range(0, len(self.cles)):
                        ligne.append(trans[self.cles[cle]])
                    lignes.append(ligne)

            with DossierDestination(imports.chemin_cannexes).writer(nom_csv) as fichier_writer:
                ligne = []
                for cle in self.cles:
                    ligne.append(pt[cle])
                fichier_writer.writerow(ligne)

                for ligne in lignes:
                    fichier_writer.writerow(ligne)
