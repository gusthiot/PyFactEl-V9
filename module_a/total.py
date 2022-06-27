from core import (Format,
                  DossierDestination)


class Total(object):
    """
    Classe pour la création du bilan des factures
    """

    cles = ['invoice-id', 'proj-nbr-0', 'proj-name-0', 'total-fact']

    def __init__(self, imports, transactions_1, sommes_1, csv_fichiers):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_1: transactions 1 générées
        :param sommes_1: sommes des transactions 1
        :param csv_fichiers: fichiers csv et nom du fichier zip par client
        """
        pt = imports.paramtexte.donnees
        self.csv_fichiers = csv_fichiers

        self.nom = "Total_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for code, par_client in sommes_1.par_client.items():
            client = imports.clients.donnees[code]
            nom_zip = "Annexes_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                      Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(code) + "_" + \
                      client['abrev_labo'] + ".zip"
            nom_csv = "Total_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                      Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + \
                      client['abrev_labo'] + ".csv"
            lignes = []

            for id_fact, par_fact in par_client['factures'].items():
                base = transactions_1.valeurs[par_fact['transactions'][0]]
                intype = base['invoice-type']
                total = par_fact['total']
                if intype == "GLOB":
                    nbr = 0
                    nom = ""
                else:
                    nbr = base['proj-nbr']
                    nom = base['proj-name']

                lignes.append([id_fact, nbr, nom, round(2*total, 1)/2])

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
