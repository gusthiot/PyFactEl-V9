from core import (Interface,
                  Format,
                  ErreurConsistance)


class Paramtexte(object):
    """
     Classe pour les labels
     """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-project', 'invoice-id', 'invoice-ref',
            'platf-code', 'platf-op', 'platf-name', 'client-code', 'client-sap', 'client-name', 'client-idclass',
            'client-class', 'client-labelclass', 'oper-id', 'oper-name', 'oper-note', 'oper-PO', 'staff-note',
            'mach-id', 'mach-name', 'mach-extra', 'user-id', 'user-sciper', 'user-name', 'user-first', 'user-name-f',
            'proj-id', 'proj-nbr', 'proj-name', 'proj-expl', 'flow-type', 'flow-cae', 'flow-noshow', 'flow-lvr',
            'flow-srv', 'item-id', 'item-idsap', 'item-codeK', 'item-textK', 'item-text2K', 'item-K1', 'item-K1a',
            'item-K1b', 'item-K2', 'item-K2a', 'item-K3', 'item-K3a', 'item-K4', 'item-K4a', 'item-K5', 'item-K5a',
            'item-K6', 'item-K6a', 'item-K7', 'item-K7a', 'item-nbr', 'item-name', 'item-unit', 'item-codeD',
            'item-flag-usage', 'item-flag-conso', 'item-eligible', 'item-order', 'item-labelcode', 'item-extra',
            'transac-date', 'transac-quantity', 'transac-usage', 'transac-runtime', 'transac-runcae', 'valuation-price',
            'valuation-brut', 'discount-type', 'discount-HC', 'discount-LVR', 'discount-CHF', 'deduct-CHF',
            'valuation-net', 'subsid-code', 'subsid-name', 'subsid-start', 'subsid-end', 'subsid-ok', 'subsid-pourcent',
            'subsid-maxproj', 'subsid-maxmois', 'subsid-reste', 'subsid-CHF', 'subsid-deduct', 'discount-bonus',
            'subsid-bonus', 'total-fact', 'runtime-N', 'runtime-avg', 'runtime-stddev', 'conso-propre-march-expl',
            'conso-propre-extra-expl', 'conso-propre-march-proj', 'conso-propre-extra-proj', 'year', 'month', 'day',
            'week-nbr', 'subsid-alrdygrant', 'your-ref', 'stat-nbuser-d', 'stat-nbuser-w', 'stat-nbuser-m',
            'stat-nbuser-3m', 'stat-nbuser-6m', 'stat-nbuser-12m', 'stat-trans', 'stat-run', 'stat-hmach',
            'date-start-y', 'date-start-m', 'date-end-y', 'date-end-m', 'version-last', 'version-change',
            'version-old-amount', 'version-new-amount', 'annex-client-titre1', 'annex-client-titre2',
            'annex-client-abrev-platform', 'annex-client-proj-no', 'annex-client-name-platform', 'annex-client-user',
            'annex-client-start', 'annex-client-end', 'annex-client-prestation', 'annex-client-quantity',
            'annex-client-unit', 'annex-client-unit-price', 'annex-client-deducted', 'annex-client-total-CHF',
            'annex-client-subtotal', 'annex-client-total', 'annex-client-pied-page-g1', 'annex-client-pied-page-g2',
            'annex-compte-titre1', 'annex-compte-titre2', 'annex-compte-abrev-platform', 'annex-compte-name-platform',
            'annex-compte-proj-no', 'annex-compte-user', 'annex-compte-start', 'annex-compte-end',
            'annex-compte-prestation', 'annex-compte-quantity', 'annex-compte-unit', 'annex-compte-unit-price',
            'annex-compte-total-CHF', 'annex-compte-subtotal', 'annex-compte-total', 'annex-compte-pied-page-g1',
            'annex-compte-pied-page-g2', 'fact-A', 'fact-B', 'fact-C', 'fact-D', 'fact-E', 'fact-F', 'fact-G',
            'fact-H', 'fact-I', 'fact-J', 'fact-K', 'fact-L', 'fact-M', 'fact-N', 'fact-O', 'fact-P', 'fact-Q',
            'fact-R', 'fact-S', 'fact-T', 'fact-U', 'fact-V', 'fact-W', 'fact-X', 'fact-Y', 'fact-Z', 'fact-AA',
            'fact-AB', 'fact-AC', 'fact-AD', 'fact-AE', 'fact-AF', 'fact-AG', 'fact-AH', 'fact-AI', 'fact-AJ',
            'fact-AK', 'fact-AL', 'fact-AM', 'fact-AN', 'fact-AO', 'fact-AP', 'fact-AQ', 'fact-AR', 'fact-AS',
            'fact-AT', 'fact-AU', 'fact-AV', 'fact-AW', 'fact-AX', 'fact-AY']
    nom_fichier = "paramtext.csv"
    libelle = "Paramètres de Texte"

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        fichier_reader = dossier_source.reader(self.nom_fichier)
        self.donnees = {}
        labels = []
        try:
            for ligne in fichier_reader:
                if len(ligne) != 2:
                    Interface.fatal(ErreurConsistance(),
                                    self.libelle + ": nombre de colonnes incorrect : " + str(len(ligne)) +
                                    ", attendu : 2")
                if ligne[0] in labels:
                    Interface.fatal(ErreurConsistance(),
                                    self.libelle + ": le label '" + ligne[0] + "' n'est pas unique\n")

                ligne[0], err = Format.est_un_alphanumerique(ligne[0], "le label", chevrons=True)
                if err != "":
                    Interface.fatal(ErreurConsistance(), self.libelle + ": " + err)

                ligne[1], err = Format.est_un_texte(ligne[1], "l'entête")
                if err != "":
                    Interface.fatal(ErreurConsistance(), self.libelle + ": pour le label '" + ligne[0] + "', " + err)

                labels.append(ligne[0])
                self.donnees[ligne[0]] = ligne[1]

            for cle in self.cles:
                if cle not in labels:
                    Interface.fatal(ErreurConsistance(),
                                    self.libelle + ": la clé '" + cle + "' n'est pas présente dans paramtext.csv")

        except IOError as e:
            Interface.fatal(e, "impossible d'ouvrir le fichier : "+self.nom_fichier)
