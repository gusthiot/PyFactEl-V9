from imports.import_d import ImportD
from core import (Outils,
                  DossierDestination)
from module_d import (Articles,
                      Tarifs,
                      Transactions3)


class ModuleD(object):

    @staticmethod
    def run(dossier_source):
        import_d = ImportD(dossier_source)
        dossier_prix = Outils.chemin([import_d.chemin_enregistrement, "Prix"], import_d.edition)
        articles = Articles(import_d)
        tarifs = Tarifs(import_d)
        if not Outils.existe(dossier_prix, True):
            articles.csv(DossierDestination(dossier_prix), import_d.paramtexte)
            tarifs.csv(DossierDestination(dossier_prix), import_d.paramtexte)

        dossier_bilans = Outils.chemin([import_d.chemin_version, "Bilans_Stats"], import_d.edition)
        Outils.existe(dossier_bilans, True)
        transactions = Transactions3(import_d, import_d.version, articles, tarifs)
        transactions.csv(DossierDestination(dossier_bilans))

        # dossier_lien = Outils.lien_dossier([import_d.facturation.lien, plateforme, annee, Outils.mois_string(mois)],
        #                                    import_d.facturation)
        #
        # dossier_pannexes = Outils.chemin([dossier_enregistrement, "Annexes_PDF"], import_d.facturation)
        # Outils.existe(dossier_pannexes, True)
        #
        # dossier_cannexes = Outils.chemin([dossier_version, "Annexes_CSV"], import_d.facturation)
        # Outils.existe(dossier_cannexes, True)
        #
        # dossier_out = Outils.chemin([dossier_version, "OUT"], import_d.facturation)
        # Outils.existe(dossier_out, True)
