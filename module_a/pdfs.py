from core import (Latex,
                  Format)


class Pdfs(object):
    """
    Classe pour la création des annexes PDF
    """

    def __init__(self, imports, transactions_2, sommes_2, versions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_2: transactions 2 générées
        :param sommes_2: sommes des transactions 2
        :param versions: versions des factures générées
        """
        self.imports = imports

        prefixe = "Annexe_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + "_" + \
                  str(imports.version)

        ii = 0
        for id_fact, donnee in versions.valeurs.items():
            if donnee['version-change'] == 'NEW' or donnee['version-change'] == 'CORRECTED':
                par_fact = sommes_2.par_fact[id_fact]
                intype = donnee['invoice-type']
                code = donnee['client-code']
                client = imports.clients.donnees[code]
                parties = {}
                for id_compte, par_compte in par_fact['projets'].items():
                    parties[id_compte] = self.entete(id_compte, intype) + self.table(transactions_2, par_compte, intype)

                if intype == "GLOB":
                    nom = prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_0"
                    contenu = ""
                    for id_compte, partie in parties.items():
                        contenu += partie
                        contenu += r'''\clearpage '''
                    Latex.creer_latex_pdf(nom, self.canevas(contenu))
                    Latex.finaliser_pdf(nom, imports.chemin_pannexes)
                else:
                    for id_compte, contenu in parties.items():
                        compte = imports.comptes.donnees[id_compte]
                        nom = prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_" + compte['numero']
                        Latex.creer_latex_pdf(nom, self.canevas(contenu))
                        Latex.finaliser_pdf(nom, imports.chemin_pannexes)

           # ii += 1
           # if ii > 2:
           #     break

    def entete(self, id_compte, intype):
        """
        création de l'entête d'annexe
        :param id_compte: id du compte concernée, pour une annexe compte
        :param intype: GLOB ou CPTE
        :return: entête
        """
        plateforme = self.imports.plateforme
        compte = self.imports.comptes.donnees[id_compte]
        if intype == "GLOB":
            dico = {'titre1': self.echappe('annex-client-titre1'), 'titre2': self.echappe('annex-client-titre2'),
                    'abrev': self.echappe('annex-client-abrev-platform'),
                    'nom': self.echappe('annex-client-name-platform'), 'num': self.echappe('annex-client-proj-no')}
        else:
            dico = {'titre1': self.echappe('annex-compte-titre1'), 'titre2': self.echappe('annex-compte-titre2'),
                    'abrev': self.echappe('annex-compte-abrev-platform'),
                    'nom': self.echappe('annex-compte-name-platform'), 'num': self.echappe('annex-compte-proj-no')}
        dico.update({'int_plat': Latex.echappe_caracteres(plateforme['int_plat']),
                     'abrev_plat': plateforme['abrev_plat'], 'numero': compte['numero'],
                     'intitule': Latex.echappe_caracteres(compte['intitule'])})
        return r'''\hspace{50mm} %(titre1)s \\
                    \hspace{50mm} %(titre2)s \\
                    %(abrev)s \hspace{50mm} %(num)s\\
                    %(abrev_plat)s \hspace{50mm} %(numero)s\\
                    %(intitule)s \\
                    %(nom)s \\
                    %(int_plat)s \\ ''' % dico

    def echappe(self, valeur):
        """
        pour échapper les caractères spéciaux des paramtextes
        :param valeur: clé de paramtexte
        :return: valeur échappée
        """
        return Latex.echappe_caracteres(self.imports.paramtexte.donnees[valeur])

    def table(self, transactions, par_compte, intype):
        """
        création de la table d'annexe
        :param transactions: transactions 2 générées
        :param par_compte: sommes des transactions 2 par compte
        :param intype: GLOB ou CPTE
        :return: table
        """
        if intype == "GLOB":
            dico = {'user': self.echappe('annex-client-user'), 'start': self.echappe('annex-client-start'),
                    'end': self.echappe('annex-client-end'), 'prest': self.echappe('annex-client-prestation'),
                    'quant': self.echappe('annex-client-quantity'), 'unit': self.echappe('annex-client-unit'),
                    'price': self.echappe('annex-client-unit-price'), 'total': self.echappe('annex-client-total-CHF'),
                    'sub': self.echappe('annex-client-subtotal'), 'tot': self.echappe('annex-client-total'), 'multi': 8}
            structure = r'''{c c c c c c c c c}'''
        else:
            dico = {'user': self.echappe('annex-compte-user'), 'start': self.echappe('annex-compte-start'),
                    'end': self.echappe('annex-compte-end'), 'prest': self.echappe('annex-compte-prestation'),
                    'quant': self.echappe('annex-compte-quantity'), 'unit': self.echappe('annex-compte-unit'),
                    'price': self.echappe('annex-compte-unit-price'), 'total': self.echappe('annex-compte-total-CHF'),
                    'sub': self.echappe('annex-compte-subtotal'), 'tot': self.echappe('annex-compte-total'), 'multi': 7}
            structure = r'''{ c c c c c c c c}'''

        contenu = r'''%(user)s & %(start)s & %(end)s & %(prest)s & %(quant)s & %(unit)s & %(price)s & ''' % dico
        if intype == "GLOB":
            contenu += self.echappe('annex-client-deducted') + " & "
        contenu += r''' %(total)s \\
                        \hline ''' % dico

        tot = 0
        for id_article, par_article in par_compte.items():
            article = self.imports.artsap.donnees[id_article]
            subtot = 0
            for par_item in par_article['items'].values():
                for par_user in par_item.values():
                    for key in par_user:
                        trans = transactions.valeurs[key]
                        subtot += trans['total-fact']
                        dico.update({'user': trans['user-name-f'], 'start-y': trans['date-start-y'],
                                     'start-m': Format.mois_string(trans['date-start-m']), 'end-y': trans['date-end-y'],
                                     'end-m': Format.mois_string(trans['date-end-m']),
                                     'prest': Latex.echappe_caracteres(trans['item-name']),
                                     'quant': trans['transac-quantity'], 'unit': trans['item-unit'],
                                     'price': Format.format_2_dec(trans['valuation-price']),
                                     'total': Format.format_2_dec(trans['total-fact'])})
                        contenu += r'''%(user)s & %(start-m)s.%(start-y)s & %(end-m)s.%(end-y)s & %(prest)s & %(quant)s 
                                        & %(unit)s & %(price)s & ''' % dico
                        if intype == "GLOB":
                            contenu += Format.format_2_dec(trans['deduct-CHF']) + " & "
                        contenu += r''' %(total)s \\
                                        \hline ''' % dico
            tot += subtot

            dico.update({'article': Latex.echappe_caracteres(article['intitule']),
                         'subtot': Format.format_2_dec(subtot)})
            contenu += r'''\multicolumn{%(multi)s}{l}{%(sub)s %(article)s} & %(subtot)s\\
                            \hline ''' % dico

        dico.update({'total': Format.format_2_dec(tot)})
        contenu += r'''\multicolumn{%(multi)s}{l}{%(tot)s} & %(total)s \\ ''' % dico

        return Latex.tableau(contenu, structure)

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
