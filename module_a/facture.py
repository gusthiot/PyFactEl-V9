from core import (CsvList,
                  Format)


class Facture(CsvList):
    """
    Classe contenant les méthodes nécessaires à la génération des factures
    """

    cles = ['fact-A', 'fact-B', 'fact-C', 'fact-D', 'fact-E', 'fact-F', 'fact-G', 'fact-H', 'fact-I', 'fact-J',
            'fact-K', 'fact-L', 'fact-M', 'fact-N', 'fact-O', 'fact-P', 'fact-Q', 'fact-R', 'fact-S', 'fact-T',
            'fact-U', 'fact-V', 'fact-W', 'fact-X', 'fact-Y', 'fact-Z', 'fact-AA', 'fact-AB', 'fact-AC', 'fact-AD',
            'fact-AE', 'fact-AF', 'fact-AG', 'fact-AH', 'fact-AI', 'fact-AJ', 'fact-AK', 'fact-AL', 'fact-AM',
            'fact-AN', 'fact-AO', 'fact-AP', 'fact-AQ', 'fact-AR', 'fact-AS', 'fact-AT', 'fact-AU', 'fact-AV',
            'fact-AW', 'fact-AX', 'fact-AY']

    def __init__(self, imports, versions, sommes_1):
        """
        génère la facture sous forme de csv
        :param imports: données importées
        :param versions: versions des factures générées
        :param sommes_1: sommes des transactions 1
        """
        super().__init__(imports)

        self.nom = "Facture_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                   Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        self.par_client = {}

        textes = imports.paramtexte.donnees

        for id_fact, donnee in versions.valeurs.items():
            if donnee['version-change'] != 'CANCELED' and donnee['version-new-amount'] > 0:
                code = donnee['client-code']
                intype = donnee['invoice-type']
                client = imports.clients.donnees[code]
                classe = imports.classes.donnees[client['id_classe']]
                if code not in self.par_client:
                    self.par_client[code] = {}
                self.par_client[code][id_fact] = {'factures': [], 'intype': intype, 'version': donnee['version-last']}

                poste = 0
                code_sap = client['code_sap']

                if donnee['version-change'] == 'NEW' or donnee['version-change'] == 'CORRECTED':

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

                    if classe['grille'] == "OUI":
                        grille = imports.facturation.lien + "/" + str(imports.edition.plateforme) + "/" + \
                            str(imports.edition.annee) + "/" + Format.mois_string(imports.edition.mois) + "/" + \
                            imports.plateforme['grille'] + '.pdf'
                    else:
                        grille = ""

                    lien = imports.facturation.lien + "/" + str(imports.edition.plateforme) + "/" + \
                        str(imports.edition.annee) + "/" + Format.mois_string(imports.edition.mois) + "/Annexes_PDF/"
                    lien += "Annexe_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                            Format.mois_string(imports.edition.mois) + "_" + str(donnee['version-last']) + "_" + \
                            str(id_fact) + ".pdf"  # "_" + client['abrev_labo'] + "_"
                    # if intype == "GLOB":
                    #     lien += "0.pdf"
                    # else:
                    #     for id_compte in sommes_1.par_fact[id_fact]['projets'].keys():
                    #         compte = imports.comptes.donnees[id_compte]
                    #         lien += compte['numero'] + ".pdf"

                    self.lignes.append([poste, imports.facturation.origine, genre, imports.facturation.commerciale,
                                        imports.facturation.canal, imports.facturation.secteur, "", "", code_sap,
                                        client['nom2'], client['nom3'], client['email'], code_sap, code_sap, code_sap,
                                        imports.facturation.devise, client['mode'], ref, "", "", your_ref, lien, "",
                                        grille])

                inc = 1
                date_dernier = str(imports.edition.annee) + Format.mois_string(imports.edition.mois) + \
                    str(imports.edition.dernier_jour)
                for id_compte, par_compte in sommes_1.par_fact[id_fact]['projets'].items():
                    nom = par_compte['numero']
                    poste = inc*10
                    for ordre, par_article in sorted(par_compte['items'].items()):
                        article = imports.artsap.donnees[par_article['id']]
                        net = par_article['total']
                        code_op = self.imports.plateforme['code_p'] + classe['code_n'] + str(imports.edition.annee) + \
                            Format.mois_string(imports.edition.mois) + article['code_d']

                        if donnee['version-change'] == 'NEW' or donnee['version-change'] == 'CORRECTED':
                            self.lignes.append([poste, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                                "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                                article['code_sap'], "", article['quantite'], article['unite'],
                                                article['type_prix'], net, article['type_rabais'], 0, date_dernier,
                                                self.imports.plateforme['centre'], "", self.imports.plateforme['fonds'],
                                                "", "", code_op, "", "", "", article['texte_sap'], nom])
                        description = article['code_d'] + " : " + str(article['code_sap'])
                        self.par_client[code][id_fact]['factures'].append({'poste': poste, 'nom': nom,
                                                                           'descr': description,
                                                                           'texte': article['texte_sap'],
                                                                           'net': "%.2f" % net, 'total': net,
                                                                           'compte': par_compte['numero']})
                        poste += 1
                    inc += 1
