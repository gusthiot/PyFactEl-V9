from core import (Format,
                  DossierDestination)


class AnnexeDetails(object):
    """
    Classe pour la création du csv d'annexe détails
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-id', 'platf-name', 'client-code',
            'client-name', 'oper-name', 'oper-note', 'staff-note', 'mach-name', 'user-sciper', 'user-name',
            'user-first', 'proj-nbr', 'proj-name', 'item-nbr', 'item-name', 'item-unit', 'transac-date',
            'transac-quantity', 'valuation-price', 'valuation-brut', 'discount-type', 'discount-CHF', 'valuation-net',
            'subsid-code', 'subsid-name', 'subsid-start', 'subsid-end', 'subsid-ok', 'subsid-pourcent',
            'subsid-maxproj', 'subsid-maxmois', 'subsid-reste', 'subsid-CHF', 'deduct-CHF', 'subsid-deduct',
            'total-fact', 'discount-bonus', 'subsid-bonus']

    def __init__(self, imports, transactions, par_client, numeros, chemin_destination):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_client: tri des transactions
        :param numeros: table des numéros de version
        :param chemin_destination: chemin vers la destination de sauvegarde
        """

        pt = imports.paramtexte.donnees
        self.csv_fichiers = {}

        for code in par_client.keys():

            client = imports.clients.donnees[code]
            nom_zip = "Annexes_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + "_" + \
                      str(imports.version) + code + "_" + client['abrev_labo'] + ".zip"
            prefixe_csv = "Details_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + \
                          "_" + str(imports.version)

            for icf in par_client[code]['projets']:
                tbtr = par_client[code]['projets'][icf]
                id_fact = numeros.couples[code][icf]
                nom_csv = prefixe_csv + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_" + str(icf) + ".csv"
                if code not in self.csv_fichiers:
                    self.csv_fichiers[code] = {'nom': nom_zip, 'fichiers': []}
                self.csv_fichiers[code]['fichiers'].append(nom_csv)
                ii = 0
                lignes = []
                for indice in tbtr:
                    val = transactions.valeurs[indice]
                    ligne = [imports.edition.annee, imports.edition.mois]
                    for cle in range(2, len(self.cles)):
                        if self.cles[cle] == 'invoice-id':
                            ligne.append(id_fact)
                        else:
                            ligne.append(val[self.cles[cle]])
                    lignes.append(ligne)
                    ii += 1

                with DossierDestination(chemin_destination).writer(nom_csv) as fichier_writer:
                    ligne = []
                    for cle in self.cles:
                        ligne.append(pt[cle])
                    fichier_writer.writerow(ligne)

                    for ligne in lignes:
                        fichier_writer.writerow(ligne)
