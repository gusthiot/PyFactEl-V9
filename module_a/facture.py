from core import (CsvList,
                  Format)


class Facture(CsvList):
    """
    Classe contenant les méthodes nécessaires à la génération des factures
    """

    def __init__(self, imports, versions, transactions_1, sommes_1):
        """
        génère la facture sous forme de csv
        :param imports: données importées
        :param versions: versions des factures générées
        :param transactions_1: transactions 1 générées
        :param sommes_1: sommes des transactions 1

        """
        super().__init__(imports)

        self.nom = "Facture_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                   Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        textes = self.imports.paramtexte.donnees

        for id_fact, donnee in versions.valeurs.items():
            if ((donnee['version-change'] == 'NEW' or donnee['version-change'] == 'CORRECTED')
                    and donnee['version-new-amount'] > 0):
                code = donnee['client-code']
                intype = donnee['invoice-type']
                client = imports.clients.donnees[code]
                classe = imports.classes.donnees[client['id_classe']]

                poste = 0
                code_sap = client['code_sap']

                if classe['ref_fact'] == "INT":
                    genre = imports.facturation.code_int
                else:
                    genre = imports.facturation.code_ext

                if client['ref'] != "":
                    your_ref = textes['your-ref'] + client['ref']
                else:
                    your_ref = ""

                ref = classe['ref_fact'] + "_" + str(imports.edition.annee) + "_" + \
                    Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(id_fact)

                lien = imports.facturation.lien + "/" + imports.plateforme['abrev_plat'] + "/" + \
                    str(imports.edition.annee) + "/" + Format.mois_string(imports.edition.mois) + "/Annexes_PDF/"
                lien += "Annexe_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + "_"\
                        + str(donnee['version-last']) + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_"
                if intype == "GLOB":
                    lien += "0.pdf"
                else:
                    for id_compte in sommes_1.par_fact[id_fact]['projets'].keys():
                        compte = imports.comptes.donnees[id_compte]
                        lien += compte['numero'] + ".pdf"

                if classe['grille'] == "OUI":
                    grille = imports.plateforme['grille'] + '.pdf'
                else:
                    grille = ""

                self.lignes.append([poste, imports.facturation.origine, genre, imports.facturation.commerciale,
                                    imports.facturation.canal, imports.facturation.secteur, "", "", code_sap,
                                    client['nom2'], client['nom3'], client['email'], code_sap, code_sap, code_sap,
                                    imports.facturation.devise, client['mode'], ref, "", "", your_ref, lien, "",
                                    grille])

                inc = 1
                date_dernier = str(imports.edition.annee) + Format.mois_string(imports.edition.mois) + \
                    str(imports.edition.dernier_jour)
                for id_compte, par_compte in sommes_1.par_fact[id_fact]['projets'].items():
                    compte = imports.comptes.donnees[id_compte]
                    nom = compte['numero'] + "-" + compte['intitule']
                    orders = {}
                    poste = inc*10
                    for id_article in par_compte.keys():
                        article = imports.artsap.donnees[id_article]
                        orders[article['ordre']] = id_article
                    for id_article in sorted(orders.values()):
                        article = imports.artsap.donnees[id_article]
                        net = 0
                        for key in par_compte[id_article]:
                            net += transactions_1.valeurs[key]['total-fact']
                        code_op = self.imports.plateforme['code_p'] + classe['code_n'] + str(imports.edition.annee) + \
                            Format.mois_string(imports.edition.mois) + article['code_d']

                        self.lignes.append([poste, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                            "", "", "", "", "", "", "", "", "", "", "", "", "", article['code_sap'], "",
                                            article['quantite'], article['unite'], article['type_prix'], net,
                                            article['type_rabais'], 0, date_dernier, self.imports.plateforme['centre'],
                                            "", self.imports.plateforme['fonds'], "", "", code_op, "", "", "",
                                            article['texte_sap'], nom])
                        poste += 1
                    inc += 1
