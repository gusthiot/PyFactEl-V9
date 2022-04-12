from core import (Outils,
                  VerifFormat,
                  ErreurConsistance)


class Edition(object):
    """
    Classe pour l'importation des paramètres d'édition
    """

    nom_fichier = "paramedit.csv"
    libelle = "Paramètres d'Edition"

    def __init__(self, dossier_source, plateformes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param plateformes: plateformes importées
        """
        donnees_csv = []
        msg = ""
        try:
            for ligne in dossier_source.reader(self.nom_fichier):
                donnees_csv.append(ligne)
        except IOError as e:
            Outils.fatal(e, "impossible d'ouvrir le fichier : "+self.nom_fichier)

        num = 4
        if len(donnees_csv) != num:
            Outils.fatal(ErreurConsistance(),
                         self.libelle + ": nombre de lignes incorrect : " +
                         str(len(donnees_csv)) + ", attendu : " + str(num))

        self.annee, err = VerifFormat.est_un_entier(donnees_csv[0][1], "l'année", mini=2000, maxi=2099)
        msg += err

        self.mois, err = VerifFormat.est_un_entier(donnees_csv[1][1], "le mois", mini=1, maxi=12)
        msg += err

        self.plateforme, err = VerifFormat.est_un_alphanumerique(donnees_csv[2][1], "l'id plateforme")
        msg += err

        self.filigrane, err = VerifFormat.est_un_texte(donnees_csv[3][1], "le filigrane", vide=True)
        msg += err

        jours = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.mois != 2:
            jour = jours[self.mois-1]
        else:
            if self.annee % 4 == 0:
                if self.annee % 100 == 0:
                    if self.annee % 400 == 0:
                        jour = 29
                    else:
                        jour = 28
                else:
                    jour = 29
            else:
                jour = 28
        self.dernier_jour = jour

        mois_fr = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
                   "novembre", "décembre"]
        self.mois_txt = mois_fr[self.mois-1]

        if self.plateforme not in plateformes.donnees.keys():
            msg += "l'id plateforme '" + self.plateforme + "' n'est pas référencé\n"

        if msg != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
