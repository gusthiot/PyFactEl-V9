from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)
import re


class Client(CsvImport):
    """
    Classe pour l'importation des données de Clients Cmi
    """

    cles = ['code', 'code_sap', 'abrev_labo', 'nom2', 'nom3', 'ref', 'email', 'mode', 'id_classe']
    nom_fichier = "client.csv"
    libelle = "Clients"

    def __init__(self, dossier_source, facturation, classes, module_a=False):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param facturation: paramètres de facturation
        :param classes: classes clients importées
        :param module_a: si on ne traite que le module A
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        codes = []

        for donnee in self.donnees:
            donnee['code_sap'], info = Format.est_un_alphanumerique(donnee['code_sap'], "le code client sap", ligne)
            msg += info

            if module_a:
                donnee['code'], info = Format.est_un_entier(donnee['code'], "le code client", ligne, 0)
            else:
                donnee['code'], info = Format.est_un_alphanumerique(donnee['code'], "le code client", ligne)
            msg += info
            if info == "":
                if donnee['code'] not in codes:
                    codes.append(donnee['code'])
                else:
                    msg += "le code client '" + donnee['code'] + "' de la ligne " + str(ligne) +\
                           " n'est pas unique\n"

            donnee['abrev_labo'], info = Format.est_un_alphanumerique(donnee['abrev_labo'], "l'abrev. labo", ligne)
            msg += info
            donnee['nom2'], info = Format.est_un_texte(donnee['nom2'], "le nom 2", ligne, True)
            msg += info
            donnee['nom3'], info = Format.est_un_texte(donnee['nom3'], "le nom 3", ligne, True)
            msg += info
            donnee['ref'], info = Format.est_un_texte(donnee['ref'], "la référence", ligne, True)
            msg += info

            if donnee['id_classe'] == "":
                msg += "le type de labo de la ligne " + str(ligne) + " ne peut être vide\n"
            else:
                if not donnee['id_classe'] in classes.donnees.keys():
                    msg += "le type de labo '" + donnee['id_classe'] + "' de la ligne " + str(ligne) +\
                        " n'existe pas dans les types N\n"
                else:
                    av_hc = classes.donnees[donnee['id_classe']]['avantage_HC']
                    donnee['rh'] = 1
                    donnee['bh'] = 0
                    if av_hc == 'BONUS':
                        donnee['bh'] = 1
                        donnee['rh'] = 0

            if (donnee['mode'] != "") and (donnee['mode'] not in facturation.modes):
                msg += "le mode d'envoi '" + donnee['mode'] + "' de la ligne " + str(ligne) +\
                    " n'existe pas dans les modes d'envoi généraux\n"

            if (donnee['mode'] == "MAIL") and (not re.match("[^@]+@[^@]+\.[^@]+", donnee['email'])):
                msg += "le format de l'e-mail '" + donnee['email'] + "' de la ligne " + str(ligne) +\
                    " n'est pas correct\n"

            donnees_dict[donnee['code']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
