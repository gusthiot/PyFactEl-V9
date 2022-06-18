from core import (Latex,
                  Format)
import math


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

        prefixe = "Annexe_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                  Format.mois_string(imports.edition.mois) + "_" + str(imports.version)

        for id_fact, donnee in versions.valeurs.items():
            if donnee['version-change'] == 'NEW' or donnee['version-change'] == 'CORRECTED':
                par_fact = sommes_2.par_fact[id_fact]
                intype = donnee['invoice-type']
                code = donnee['client-code']


                if code != '221640':
                    continue


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
                    Latex.creer_latex_pdf(nom, self.canevas(contenu, intype))
                    Latex.finaliser_pdf(nom, imports.chemin_pannexes)
                else:
                    for id_compte, contenu in parties.items():
                        compte = imports.comptes.donnees[id_compte]
                        nom = prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_" + compte['numero']
                        Latex.creer_latex_pdf(nom, self.canevas(contenu, intype))
                        Latex.finaliser_pdf(nom, imports.chemin_pannexes)

    def entete(self, id_compte, intype):
        """
        création de l'entête d'annexe
        :param id_compte: id du compte concernée, pour une annexe compte
        :param intype: GLOB ou CPTE
        :return: entête
        """
        contenu = ""
        if self.imports.logo != "":
            contenu += r'''
                \begin{flushleft}
                \includegraphics[height=8mm]{logo}
                \end{flushleft}
                '''
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
        contenu += r''' \begin{flushright}
                    \LARGE \textcolor{taupe}{%(titre1)s} \\
                    \LARGE \textcolor{canard}{\textbf{%(titre2)s}} \\
                    \end{flushright}
                    
                    \vspace{5mm}
                    
                    \begin{flushleft}
                    \renewcommand{\arraystretch}{1.2}
                    \begin{tabular}{p{109mm} l}
                    \small \textcolor{taupe}{%(abrev)s} & \small \textcolor{taupe}{%(num)s}\\
                    \textcolor{canard}{\textbf{%(abrev_plat)s}} & \textcolor{canard}{\textbf{%(numero)s}}\\
                     & \textcolor{canard}{\textbf{%(intitule)s}} \\
                    \small \textcolor{taupe}{%(nom)s} & \\
                    \textcolor{canard}{\textbf{%(int_plat)s}} & \\ 
                    \end{tabular}
                    \end{flushleft} 
                     ''' % dico
        return contenu

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
        structure = r'''{m{21mm} m{15mm} m{15mm} m{41mm} m{17mm} m{13mm} m{17mm}'''
        if intype == "GLOB":
            dico = {'user': self.echappe('annex-client-user'), 'start': self.echappe('annex-client-start'),
                    'end': self.echappe('annex-client-end'), 'prest': self.echappe('annex-client-prestation'),
                    'quant': self.echappe('annex-client-quantity'), 'unit': self.echappe('annex-client-unit'),
                    'price': self.echappe('annex-client-unit-price'), 'total': self.echappe('annex-client-total-CHF'),
                    'sub': self.echappe('annex-client-subtotal'), 'tot': self.echappe('annex-client-total'), 'multi': 8,
                    'taille': str(156) + "mm", 'deduct': self.echappe('annex-client-deducted')}
            structure += r'''m{17mm} '''
        else:
            dico = {'user': self.echappe('annex-compte-user'), 'start': self.echappe('annex-compte-start'),
                    'end': self.echappe('annex-compte-end'), 'prest': self.echappe('annex-compte-prestation'),
                    'quant': self.echappe('annex-compte-quantity'), 'unit': self.echappe('annex-compte-unit'),
                    'price': self.echappe('annex-compte-unit-price'), 'total': self.echappe('annex-compte-total-CHF'),
                    'sub': self.echappe('annex-compte-subtotal'), 'tot': self.echappe('annex-compte-total'), 'multi': 7,
                    'taille': str(139) + "mm"}
        structure += r''' m{25mm}}'''

        titres = r'''
                 \begin{flushleft}
                 \renewcommand{\arraystretch}{0}
                 \setlength{\arrayrulewidth}{0.5mm}
                 \arrayrulecolor{leman}
                 \begin{tabular}
                    ''' + structure + r'''
                  \flb{%(user)s} & \flb{%(start)s} & \flb{%(end)s} & \flb{%(prest)s} & \flb{%(quant)s} & 
                  \frb{%(unit)s} & \frb{%(price)s} & ''' % dico
        if intype == "GLOB":
            titres += r'''\frb{%(deduct)s} & ''' % dico
        titres += r''' \frb{%(total)s} \\
                        \hline ''' % dico

        fin = r''' \end{tabular}
                    \end{flushleft} '''

        tot = 0
        lignes = []
        for id_article, par_article in par_compte.items():
            article = self.imports.artsap.donnees[id_article]
            subtot = 0
            for par_item in par_article['items'].values():
                for par_user in par_item.values():
                    for key in par_user:
                        trans = transactions.valeurs[key]
                        qqq = 1000 * trans['transac-quantity']
                        if qqq % 1000 == 0:
                            quantite = str(int(trans['transac-quantity'])) + r'''\hphantom{.000}'''
                        elif qqq % 100 == 0:
                            quantite = str(trans['transac-quantity']) + r'''\hphantom{00}'''
                        elif qqq % 10 == 0:
                            quantite = str(trans['transac-quantity']) + r'''\hphantom{0}'''
                        else:
                            quantite = str(trans['transac-quantity'])
                        subtot += trans['total-fact']
                        dico.update({'user': trans['user-name-f'], 'start-y': trans['date-start-y'],
                                     'start-m': Format.mois_string(trans['date-start-m']), 'end-y': trans['date-end-y'],
                                     'end-m': Format.mois_string(trans['date-end-m']),
                                     'prest': Latex.echappe_caracteres(trans['item-name']),
                                     'quant': quantite, 'unit': trans['item-unit'],
                                     'price': Format.nombre(trans['valuation-price']),
                                     'deduct': Format.nombre(trans['deduct-CHF']),
                                     'total': Format.nombre(trans['total-fact'])})
                        ligne = r'''\fl{%(user)s} & \fl{%(start-m)s.%(start-y)s} & \fl{%(end-m)s.%(end-y)s} & 
                                \fl{%(prest)s} & \fr{%(quant)s} & \fr{%(unit)s} & \fr{%(price)s} & ''' % dico
                        if intype == "GLOB":
                            ligne += r'''\fr{ %(deduct)s} & ''' % dico
                        ligne += r''' \fr{%(total)s} \\''' % dico
                        lignes.append(ligne)
            tot += subtot

            dico.update({'article': Latex.echappe_caracteres(article['intitule']),
                         'subtot': Format.nombre(subtot)})
            lignes.append(r''' \hline
                            \multicolumn{%(multi)s}{m{%(taille)s}}{\flbs{%(sub)s %(article)s}} & \frbs{%(subtot)s}\\
                            \hline ''' % dico)
        first_max = 18
        then_max = 25
        contenu = titres
        boucle = 0
        max_page = first_max
        while 1:
            if boucle > 0:
                contenu += fin
                contenu += titres
            beg = boucle*max_page
            if (len(lignes)-beg) > max_page:
                end = (boucle+1)*max_page
            else:
                end = len(lignes)
            for num in range(beg, end):
                contenu += lignes[num]
            if end == len(lignes):
                break
            boucle += 1
            max_page = then_max

        dico.update({'total': Format.nombre(tot)})
        contenu += r''' \multicolumn{%(multi)s}{m{%(taille)s}}{\flbs{%(tot)s}} & \frbs{%(total)s} \\ 
                    ''' % dico
        contenu += fin
        return contenu

    def canevas(self, contenu, intype):
        """
        création du canevas latex autour du contenu
        :param contenu: contenu variable du document
        :param intype: GLOB ou CPTE
        :return: le document latex complet
        """

        document = Latex.entete()
        document += r'''
             \usepackage{multirow}
             \usepackage[table]{xcolor}
             \definecolor{leman}{RGB}{0, 167, 157}
             \definecolor{taupe}{RGB}{65, 61, 58}
             \definecolor{canard}{RGB}{0, 116, 118}
             \setlength{\tabcolsep}{0pt}
             \usepackage{graphicx}
             \usepackage{fancyhdr}
             \usepackage{lastpage}
             
             \pagestyle{fancy}
        
             \fancyhead{}
             \fancyfoot{}      
             
             \newcommand{\changefont}{%
                \fontsize{8pt}{10pt}\selectfont
             }
             
             \newcommand{\fl}[1]{\begin{flushleft}\textcolor{taupe}{#1}\end{flushleft}}
             \newcommand{\flb}[1]{\begin{flushleft}\textcolor{taupe}{\textbf{#1}}\end{flushleft}}
             \newcommand{\flbs}[1]{\begin{flushleft}\textcolor{canard}{\textbf{\small#1}}\end{flushleft}}
             \newcommand{\fr}[1]{\begin{flushright}\textcolor{taupe}{#1}\end{flushright}}
             \newcommand{\frb}[1]{\begin{flushright}\textcolor{taupe}{\textbf{#1}}\end{flushright}}
             \newcommand{\frbs}[1]{\begin{flushright}\textcolor{canard}{\textbf{\small#1}}\end{flushright}}
            
             \renewcommand{\headrulewidth}{0pt}
             \renewcommand{\footrulewidth}{0pt}
             '''

        dico = {'pied1': self.echappe('annex-compte-pied-page-g1'), 'pied2': self.echappe('annex-compte-pied-page-g2'),
                'logo': self.imports.chemin_logo,
                'filigrane': Latex.echappe_caracteres(self.imports.edition.filigrane[:15])}
        if intype != "GLOB":
            document += r'''\fancyfoot[L]{\changefont %(pied1)s \\ %(pied2)s}''' % dico

        document += r'''
             \fancyfoot[C]{\changefont Page \thepage\  of \pageref{LastPage}}
             \fancyfoot[R]{\changefont \today}
             '''
        if self.imports.logo != "":
            document += r'''
                \graphicspath{ {%(logo)s/} }''' % dico

        if self.imports.edition.filigrane != "":
            document += r'''
                \usepackage{draftwatermark}
                \SetWatermarkLightness{0.8}
                \SetWatermarkAngle{45}
                \SetWatermarkScale{2}
                \SetWatermarkFontSize{2cm}
                \SetWatermarkText{%(filigrane)s}
                ''' % dico

        document += r'''
            \begin{document}
            \changefont
            '''

        document += contenu

        document += r'''
            \end{document}
            '''

        return document
