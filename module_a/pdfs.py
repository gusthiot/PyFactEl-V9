from core import (Latex,
                  Format)


class Pdfs(object):
    """
    Classe pour la création des annexes PDF
    """

    def __init__(self, imports, transactions, versions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param versions: versions des factures générées
        """
        self.imports = imports

        prefixe = "Annexe_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + "_" + \
                  str(imports.version)
        for id_fact, donnee in versions.valeurs.items():
            if donnee['version-change'] != 'IDEM':
                par_fact = versions.facts_new[id_fact]
                total = 0
                base = None
                code = donnee['client-code']
                est_client = False
                parties = {}
                for id_compte, par_compte in par_fact['projets'].items():
                    for par_article in par_compte.values():
                        for par_item in par_article.values():
                            for par_user in par_item.values():
                                for key in par_user:
                                    trans = transactions.valeurs[key]
                                    if not base:
                                        base = trans
                                    total += trans['total-fact']
                    # print(id_fact, base['proj-id'], v['version-change'], total)

                    parties[id_compte] = r'''Hello World !!!'''

                    if base['invoice-type'] == "GLOB":
                        est_client = True

                client = imports.clients.donnees[code]
                if est_client:
                    nom = prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_0"
                    contenu = ""
                    for id_compte, partie in parties.items():
                        contenu += partie
                    Latex.creer_latex_pdf(nom, self.canevas(contenu))
                    Latex.finaliser_pdf(nom, imports.chemin_pannexes)
                else:
                    for id_compte, contenu in parties.items():
                        compte = imports.comptes.donnees[id_compte]
                        nom = prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_" + compte['numero']
                        Latex.creer_latex_pdf(nom, self.canevas(contenu))
                        Latex.finaliser_pdf(nom, imports.chemin_pannexes)

    def canevas(self, contenu):
        """
        création du canevas latex autour du contenu
        :param contenu: contenu variable du document
        :return: le document latex complet
        """

        document = Latex.entete()
        # document += r'''
        #     \usepackage[margin=12mm, includehead, includefoot]{geometry}
        #     \usepackage{multirow}
        #     \usepackage{graphicx}
        #     \usepackage{longtable}
        #     \usepackage{dcolumn}
        #     \usepackage{changepage}
        #     \usepackage[scriptsize]{caption}
        #     \captionsetup[table]{position=bottom}
        #     \usepackage{fancyhdr}\usepackage{float}
        #     \restylefloat{table}
        #
        #     '''

        if self.imports.edition.filigrane != "":
            document += r'''
                \usepackage{draftwatermark}
                \SetWatermarkLightness{0.8}
                \SetWatermarkAngle{45}
                \SetWatermarkScale{2}
                \SetWatermarkFontSize{2cm}
                \SetWatermarkText{''' + self.imports.edition.filigrane[:15] + r'''}
                '''

        # document += r'''
        #     \pagestyle{fancy}
        #
        #     \fancyhead{}
        #     \fancyfoot{}
        #
        #     \renewcommand{\headrulewidth}{0pt}
        #     \renewcommand{\footrulewidth}{0pt}
        #     \renewcommand{\arraystretch}{1.5}
        #
        #     \fancyhead[L]{\leftmark}
        #     \fancyhead[R]{\thepage \\ \rightmark}
        #
        #     \newcommand{\fakesection}[2]{
        #         \markboth{#1}{#2}
        #     }'''
        document += r'''
            \begin{document}
            '''

        document += contenu

        document += r'''
            \end{document}
            '''

        return document
