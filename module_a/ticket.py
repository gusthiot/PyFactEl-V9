from core import Format
import os


class Ticket(object):
    """
    Classe contenant les méthodes nécessaires à la génération des tickets
    """

    def __init__(self, imports, factures, sommes_1):
        """
        génère les tickets sous forme de sections html
        :param imports: données importées
        :param factures: factures générées
        :param sommes_1: sommes des transactions 1
        """

        self.nom = "Ticket_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                   Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".html"

        self.sections = {}

        textes = imports.paramtexte.donnees

        for code, par_client in sommes_1.par_client.items():
            client = imports.clients.donnees[code]
            classe = imports.classes.donnees[client['id_classe']]

            if client['ref'] != "":
                your_ref = textes['your-ref'] + client['ref']
            else:
                your_ref = ""

            total = 0
            dico_contenu = {'code': code, 'abrev': client['abrev_labo'], 'nom2': client['nom2'],
                            'nom3': client['nom3'], 'ref': your_ref}

            contenu_client = r'''<section id="%(code)s">
                                    <section>
                                        <div id="entete">
                                            %(code)s <br />
                                            %(abrev)s <br />
                                            %(nom2)s <br />
                                            %(nom3)s <br />
                                        </div><br />
                                        ''' % dico_contenu
            contenu_client += r'''      <div id="reference">%(ref)s</div>
                                        <table id="tableau">
                                            <tr>
                                                <td> Description </td>
                                                <td> Net amount <br /> [CHF] </td>
                                            </tr>
                                            ''' % dico_contenu

            for ordre, par_article in sorted(par_client['articles'].items()):
                article = imports.artsap.donnees[par_article['id']]
                total += par_article['total']
                description = article['code_d'] + " : " + str(article['code_sap'])
                dico_art = {'descr': description, 'texte': article['texte_sap'], 'net': "%.2f" % par_article['total']}
                contenu_client += r'''     <tr>
                                                <td> %(descr)s <br /> %(texte)s </td>
                                                <td id="toright"> %(net)s </td>
                                            </tr>
                                            ''' % dico_art

            dico_contenu.update({'total': "%.2f" % total})
            contenu_client += r'''          <tr>
                                                <td id="toright">Total [CHF] : </td>
                                                <td id="toright">%(total)s</td>
                                            </tr>
                                        </table>
                                        ''' % dico_contenu
            nom_zip = "Annexes_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                      Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(code) + "_" + \
                      client['abrev_labo'] + ".zip"
            dossier_zip = "./Annexes_CSV/" + nom_zip
            chemin_zip = imports.chemin_cannexes + "/" + nom_zip

            if os.path.isfile(chemin_zip):
                contenu_client += r'''  <table id="annexes">
                                            <tr>
                                                <td>
                                                    <a href="''' + dossier_zip + r'''" target="new">
                                                    ''' + nom_zip + r'''</a>
                                                </td>
                                            </tr>
                                        </table>
                                    '''
            contenu_client += r'''
                                    </section>
                                    '''
            if code in factures.par_client:
                for id_fact, par_fact in factures.par_client[code].items():
                    reference = classe['ref_fact'] + "_" + str(imports.edition.annee) + "_" + \
                        Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(id_fact)
                    contenu_client += r'''  <section>
                                                ''' + reference + r''' <br /><br />
                                                <table id="tableau">
                                                    <tr>
                                                        <td>N° Poste </td>
                                                        <td> Name </td>
                                                        <td> Description </td>
                                                        <td> Net amount <br /> [CHF] </td>
                                                    </tr>
                                                    '''
                    total = 0
                    # num_compte = 0
                    for dico_fact in par_fact['factures']:
                        total += dico_fact['total']
                        # num_compte = dico_fact['compte']
                        contenu_client += r'''      <tr>
                                                        <td>%(poste)s</td>
                                                        <td>%(nom)s</td>
                                                        <td> %(descr)s <br /> %(texte)s </td>
                                                        <td id="toright">%(net)s</td>
                                                    </tr>
                                                    ''' % dico_fact
                    dico_contenu.update({'total': "%.2f" % total})
                    contenu_client += r'''          <tr>
                                                        <td colspan="3" id="toright">Total [CHF] : </td>
                                                        <td id="toright">%(total)s</td>
                                                    </tr>
                                                </table> 
                                            ''' % dico_contenu

                    prefixe_pdf = "Annexe_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                                  "_" + Format.mois_string(imports.edition.mois) + "_" + str(par_fact['version'])
                    nom_pdf = prefixe_pdf + "_" + str(id_fact) + ".pdf"
                    # if par_fact['intype'] == "GLOB":
                    #     nom_pdf = prefixe_pdf + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_0.pdf"
                    # else:
                    #     nom_pdf = prefixe_pdf + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_" + num_compte\
                    #               + ".pdf"

                    dossier_pdf = "../Annexes_PDF/" + nom_pdf
                    chemin_pdf = imports.chemin_pannexes + "/" + nom_pdf

                    if os.path.isfile(chemin_pdf):
                        contenu_client += r'''  <table id="annexes">
                                                    <tr>
                                                        <td>
                                                            <a href="''' + dossier_pdf + r'''" target="new">
                                                            ''' + nom_pdf + r'''</a>
                                                        </td>
                                                    </tr>
                                                </table>
                                            '''
                    contenu_client += r''' 
                                    </section>
                                '''
            contenu_client += r''' 
                                </section>
                                '''

            self.sections[client['abrev_labo'] + " (" + str(code) + ")"] = contenu_client

    def creer_html(self, destination):
        """
        crée une page html autour d'une liste de sections
        :param destination:  Une instance de la classe dossier.DossierDestination
        """

        with destination.open(self.nom) as fichier:
            html = r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                    <head>
                        <meta content="text/html; charset=cp1252" http-equiv="content-type" />
                        <meta content="EPFL" name="author" />
                        <style>
                        #entete {
                            margin-left: 600px;
                            text-align:left;
                        }
                        #tableau {
                            border-collapse: collapse;
                            margin: 20px;
                        }
                        #tableau tr, #tableau td {
                            border: 1px solid black;
                            vertical-align:middle;
                        }
                        #tableau td {
                            padding: 3px;
                        }
                        #annexes tr, #annexes td {
                            border: 0px;
                        }
                        #annexes td {
                            padding: 3px;
                        }
                        #toright {
                            text-align:right;
                        }
                        #combo {
                            margin-top: 10px;
                            margin-left: 50px;
                        }
                        #reference {
                            text-align:left;
                            margin-left: 20px;
                        }
                        </style>
                        <link rel="stylesheet" href="../css/reveal.css">
                        <link rel="stylesheet" href="../css/white.css">
                    </head>
                    <body>
                        <div id="combo">
                            <select name="client" onchange="changeClient(this)">
                            '''
            i = 0
            for client in sorted(self.sections.keys()):
                html += r'''<option value="''' + str(i) + r'''">''' + client + r'''</option>'''
                i += 1
            html += r'''
                            </select>
                        </div>
                        <div class="reveal">
                          <div class="slides">
                '''
            for client, section in sorted(self.sections.items()):
                html += section
            html += r'''
                          </div>
                        </div>
                        <script src="../js/reveal.js"></script>
                        <script>
                            Reveal.initialize();
                        </script>
                        <script>
                            function changeClient(sel) {
                                Reveal.slide(sel.value, 0);
                            }
                        </script>
                    </body>
                </html>'''
            fichier.write(html)
