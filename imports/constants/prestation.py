from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Prestation(CsvImport):
    """
    Classe pour l'importation des données de Prestations du catalogue
    """

    cles = ['annee', 'mois', 'id_prestation', 'no_prestation', 'designation', 'id_article', 'unite_prest', 'prix_unit',
            'id_plateforme', 'id_machine']
    nom_fichier = "prestation.csv"
    libelle = "Prestations"

    def __init__(self, dossier_source, artsap, coefprests, plateformes, machines, edition):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param artsap: articles SAP importés
        :param coefprests: coefficients prestations importés
        :param plateformes: plateformes importées
        :param machines: machines importées
        :param edition: paramètres d'édition
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['mois'], info = Format.est_un_entier(donnee['mois'], "le mois ", ligne, 1, 12)
            msg += info
            donnee['annee'], info = Format.est_un_entier(donnee['annee'], "l'annee ", ligne, 2000, 2099)
            msg += info
            if donnee['mois'] != edition.mois or donnee['annee'] != edition.annee:
                msg += "date incorrect ligne " + str(ligne) + "\n"

            donnee['id_prestation'], info = Format.est_un_alphanumerique(donnee['id_prestation'], "l'id prestation",
                                                                         ligne)
            msg += info
            if info == "":
                if donnee['id_prestation'] not in ids:
                    ids.append(donnee['id_prestation'])
                else:
                    msg += "l'id prestation '" + donnee['id_prestation'] + "' de la ligne " + str(ligne) +\
                           " n'est pas unique\n"

            if donnee['no_prestation'] == "":
                msg += "le numéro de prestation de la ligne " + str(ligne) + " ne peut être vide\n"
            else:
                donnee['no_prestation'], info = Format.est_un_alphanumerique(donnee['no_prestation'],
                                                                             "le no prestation", ligne)
                msg += info

            donnee['designation'], info = Format.est_un_texte(donnee['designation'], "la désignation", ligne)
            msg += info
            donnee['unite_prest'], info = Format.est_un_texte(donnee['unite_prest'], "l'unité prestation", ligne, True)
            msg += info

            if donnee['id_article'] == "":
                msg += "l'id article SAP  de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_article'] not in artsap.donnees.keys():
                msg += "l'id article SAP de la ligne " + str(ligne) + " n'existe pas dans les codes D\n"
            elif not coefprests.contient_article(donnee['id_article']):
                msg += "l'id article SAP' '" + donnee['id_article'] + "' de la ligne " + str(ligne) +\
                       " n'est pas référencée dans les coefficients\n"

            msg += self._test_id_coherence(donnee['id_plateforme'], "l'id plateforme", ligne, plateformes)

            msg += self._test_id_coherence(donnee['id_machine'], "l'id machine", ligne, machines, True)

            donnee['prix_unit'], info = Format.est_un_nombre(donnee['prix_unit'], "le prix unitaire", ligne, 2, 0)
            msg += info

            del donnee['annee']
            del donnee['mois']
            donnees_dict[donnee['id_prestation']] = donnee
            ligne += 1

        self.donnees = donnees_dict
        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
