from imports.import_d import ImportD
from core import (Outils,
                  DossierDestination)
from module_d import (Articles,
                      Tarifs)


class ModuleD(object):

    @staticmethod
    def run(dossier_source):
        import_d = ImportD(dossier_source)
        mois = import_d.edition.mois
        annee = import_d.edition.annee
        plateforme = import_d.edition.plateforme

        if import_d.edition.filigrane != "":
            chemin = import_d.generaux.chemin_filigrane
        else:
            chemin = import_d.generaux.chemin
        dossier_enregistrement = Outils.chemin([chemin, plateforme, annee, Outils.mois_string(mois)], import_d.generaux)
        existe = Outils.existe(dossier_enregistrement, True)
        dossier_lien = Outils.lien_dossier([import_d.generaux.lien, plateforme, annee, Outils.mois_string(mois)],
                                           import_d.generaux)
        """
        if existe:
            msg = "Le répertoire " + dossier_enregistrement + " existe déjà !"
            Outils.affiche_message(msg)
            sys.exit("Erreur sur le répértoire")
        """

        dossier_annexes_pdf = Outils.chemin([dossier_enregistrement, "Annexes_PDF"], import_d.generaux)
        Outils.existe(dossier_annexes_pdf, True)
        dossier_in = Outils.chemin([dossier_enregistrement, "IN"], import_d.generaux)
        if not Outils.existe(dossier_in, True):
            import_d.copie_fixes(DossierDestination(dossier_in))
        dossier_prix = Outils.chemin([dossier_enregistrement, "Prix"], import_d.generaux)
        if not Outils.existe(dossier_prix, True):
            articles = Articles(import_d)
            articles.csv(DossierDestination(dossier_prix), import_d.paramtexte)
            tarifs = Tarifs(import_d)
            tarifs.csv(DossierDestination(dossier_prix), import_d.paramtexte)


        version = 0
        while True:
            dossier_version = Outils.chemin([dossier_enregistrement, "V"+str(version)], import_d.generaux)
            if Outils.existe(dossier_version, True):
                version = version + 1
            else:
                break
        dossier_vin = Outils.chemin([dossier_version, "IN"], import_d.generaux)
        Outils.existe(dossier_vin, True)
        import_d.copie_variables(DossierDestination(dossier_vin))
