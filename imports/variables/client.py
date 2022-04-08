from imports import Fichier
from core import (Outils, ErreurCoherence)
import re


class Client(Fichier):
    """
    Classe pour l'importation des données de Clients Cmi
    """

    cles = ['code', 'code_sap', 'abrev_labo', 'nom2', 'nom3', 'ref', 'email', 'mode', 'id_classe']
    nom_fichier = "client.csv"
    libelle = "Clients"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.codes = []

    def obtenir_codes(self):
        """
        retourne les codes de tous les clients
        :return: codes de tous les clients
        """
        if self.verifie_coherence == 0:
            Outils.fatal(ErreurCoherence(),
                         self.libelle + ": la consistance de " + self.nom_fichier +
                         " doit être vérifiée avant d'en utiliser les données")
        return self.codes

    def est_coherent(self, generaux, classes):
        """
        vérifie que les données du fichier importé sont cohérentes, et efface les colonnes mois et année
        :param generaux: paramètres généraux
        :param classes: classes clients importées
        :return: 1 s'il y a une erreur, 0 sinon
        """

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}

        for donnee in self.donnees:
            donnee['code_sap'], info = Outils.est_un_alphanumerique(donnee['code_sap'], "le code client sap", ligne)
            msg += info

            donnee['code'], info = Outils.est_un_alphanumerique(donnee['code'], "le code client", ligne)
            msg += info
            if info == "":
                if donnee['code'] not in self.codes:
                    self.codes.append(donnee['code'])
                else:
                    msg += "le code client '" + donnee['code'] + "' de la ligne " + str(ligne) +\
                           " n'est pas unique\n"

            donnee['abrev_labo'], info = Outils.est_un_alphanumerique(donnee['abrev_labo'], "l'abrev. labo", ligne)
            msg += info
            donnee['nom2'], info = Outils.est_un_texte(donnee['nom2'], "le nom 2", ligne, True)
            msg += info
            donnee['nom3'], info = Outils.est_un_texte(donnee['nom3'], "le nom 3", ligne, True)
            msg += info
            donnee['ref'], info = Outils.est_un_texte(donnee['ref'], "la référence", ligne, True)
            msg += info

            if donnee['id_classe'] == "":
                msg += "le type de labo de la ligne " + str(ligne) + " ne peut être vide\n"
            else:
                classe = classes.contient_id(donnee['id_classe'])
                if not classe:
                    msg += "le type de labo '" + donnee['id_classe'] + "' de la ligne " + str(ligne) +\
                        " n'existe pas dans les types N\n"
                else:
                    av_hc = classe['avantage_HC']
                    donnee['rh'] = 1
                    donnee['bh'] = 0
                    if av_hc == 'BONUS':
                        donnee['bh'] = 1
                        donnee['rh'] = 0

            if (donnee['mode'] != "") and (donnee['mode'] not in generaux.obtenir_modes_envoi()):
                msg += "le mode d'envoi '" + donnee['mode'] + "' de la ligne " + str(ligne) +\
                    " n'existe pas dans les modes d'envoi généraux\n"

            if (donnee['mode'] == "MAIL") and (not re.match("[^@]+@[^@]+\.[^@]+", donnee['email'])):
                msg += "le format de l'e-mail '" + donnee['email'] + "' de la ligne " + str(ligne) +\
                    " n'est pas correct\n"

            donnees_dict[donnee['code']] = donnee

            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
