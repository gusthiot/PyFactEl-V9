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

        dossier_in = Outils.chemin([import_d.dossier_enregistrement, "IN"], import_d.generaux)
        if not Outils.existe(dossier_in, True):
            import_d.copie_fixes(DossierDestination(dossier_in))

        dossier_prix = Outils.chemin([import_d.dossier_enregistrement, "Prix"], import_d.generaux)
        articles = Articles(import_d)
        tarifs = Tarifs(import_d)
        if not Outils.existe(dossier_prix, True):
            articles.csv(DossierDestination(dossier_prix), import_d.paramtexte)
            tarifs.csv(DossierDestination(dossier_prix), import_d.paramtexte)

        version = 0
        while True:
            dossier_version = Outils.chemin([import_d.dossier_enregistrement, "V"+str(version)], import_d.generaux)
            if Outils.existe(dossier_version, True):
                version = version + 1
            else:
                break
        dossier_vin = Outils.chemin([dossier_version, "IN"], import_d.generaux)
        Outils.existe(dossier_vin, True)
        import_d.copie_variables(DossierDestination(dossier_vin))

        dossier_bilans = Outils.chemin([dossier_version, "Bilans_Stats"], import_d.generaux)
        Outils.existe(dossier_bilans, True)
        transactions = Transactions3(import_d, version, articles, tarifs)
        transactions.csv(DossierDestination(dossier_bilans))

        # dossier_lien = Outils.lien_dossier([import_d.generaux.lien, plateforme, annee, Outils.mois_string(mois)],
        #                                    import_d.generaux)
        #
        # dossier_pannexes = Outils.chemin([dossier_enregistrement, "Annexes_PDF"], import_d.generaux)
        # Outils.existe(dossier_pannexes, True)
        #
        # dossier_cannexes = Outils.chemin([dossier_version, "Annexes_CSV"], import_d.generaux)
        # Outils.existe(dossier_cannexes, True)
        #
        # dossier_out = Outils.chemin([dossier_version, "OUT"], import_d.generaux)
        # Outils.existe(dossier_out, True)
