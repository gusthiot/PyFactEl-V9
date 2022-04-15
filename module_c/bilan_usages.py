from core import Outils
import math


class BilanUsages(object):
    """
    Classe pour la création du csv de bilan d'usage
    """

    cles = ['invoice-year', 'invoice-month', 'platf-code', 'platf-name', 'item-id', 'item-nbr', 'item-name',
            'item-unit', 'transac-usage', 'transac-runtime', 'runtime-N', 'runtime-avg', 'runtime-stddev']

    def __init__(self, imports, transactions, par_item):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_item: tri des transactions
        """
        self.imports = imports
        self.plateforme = imports.plateformes.donnees[imports.edition.plateforme]

        self.nom = "Bilan-usage_" + str(self.plateforme['abrev_plat']) + "_" + str(imports.edition.annee) + "_" + \
                   Outils.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        self.lignes = []
        ii = 0
        trans_vals = transactions.valeurs
        for item in par_item.keys():
            tbtr = par_item[item]
            base = trans_vals[tbtr[0]]
            if base['item-flag-usage'] == "OUI":
                ligne = [imports.edition.annee, imports.edition.mois]
                for cle in range(2, len(self.cles)-5):
                    ligne.append(base[self.cles[cle]])
                usage = 0
                runtime = 0
                nn = 0
                avg = 0
                stddev = 0
                rts = []
                for indice in tbtr:
                    trans = trans_vals[indice]
                    if (imports.edition.annee == trans['transac-date'].year and
                            imports.edition.mois == trans['transac-date'].month):
                        usage += trans['transac-usage']
                        if trans['transac-runtime'] != "":
                            rti = trans['transac-runtime']
                            runtime += rti
                            nn += 1
                            rts.append(rti)
                if nn > 0:
                    avg = runtime / nn
                    somme = 0
                    for rt in rts:
                        somme += math.pow(rt-avg, 2)
                    stddev = math.sqrt(1 / nn * somme)
                ligne += [round(usage, 4), round(runtime, 4), nn, round(avg, 4), round(stddev, 4)]
                self.lignes.append(ligne)
                ii += 1

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
