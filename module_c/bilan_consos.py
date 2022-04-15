from core import Outils


class BilanConsos(object):
    """
    Classe pour la création du csv de bilan de consommation propre
    """

    cles = ['invoice-year', 'invoice-month', 'platf-code', 'platf-name', 'proj-id', 'proj-nbr', 'proj-name',
            'proj-expl', 'item-id', 'item-nbr', 'item-name', 'item-unit', 'item-idsap', 'item-codeD', 'item-extra',
            'mach-extra', 'conso-propre-march-expl', 'conso-propre-extra-expl', 'conso-propre-march-proj',
            'conso-propre-extra-proj']

    def __init__(self, imports, transactions, par_projet):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_projet: tri des transactions
        """
        self.imports = imports
        self.plateforme = imports.plateformes.donnees[imports.edition.plateforme]

        self.nom = "Bilan-conso-propre_" + str(self.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + \
                   "_" + Outils.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        self.lignes = []
        for id_projet in par_projet.keys():
            par_item = par_projet[id_projet]
            for item in par_item.keys():
                tbtr = par_item[item]
                base = transactions.valeurs[tbtr[0]]
                if base['item-flag-conso'] == "OUI":
                    ligne = [imports.edition.annee, imports.edition.mois]
                    for cle in range(2, len(self.cles) - 4):
                        ligne.append(base[self.cles[cle]])
                    goops = 0
                    extrops = 0
                    goint = 0
                    extrint = 0
                    for indice in tbtr:
                        trans = transactions.valeurs[indice]
                        if (imports.edition.annee == trans['transac-date'].year and
                                imports.edition.mois == trans['transac-date'].month):
                            net = trans['valuation-net']
                            if trans['client-code'] == trans['platf-code']:
                                if trans['item-extra'] == "TRUE":
                                    if trans['proj-expl'] == "TRUE":
                                        extrops += net
                                    else:
                                        extrint += net
                                else:
                                    if trans['proj-expl'] == "TRUE":
                                        goops += net
                                    else:
                                        goint += net
                    if goops > 0 or extrops > 0 or goint > 0 or extrint > 0:
                        ligne += [round(goops, 2), round(extrops, 2), round(goint, 2), round(extrint, 2)]
                        self.lignes.append(ligne)

    def csv(self, dossier_destination):
        """
        création du fichier csv à partir de la liste des noms de colonnes
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """

        pt = self.imports.paramtexte.donnees

        with dossier_destination.writer(self.nom) as fichier_writer:
            ligne = []
            for cle in self.cles:
                ligne.append(pt[cle])
            fichier_writer.writerow(ligne)

            for ligne in self.lignes:
                fichier_writer.writerow(ligne)
