from core import (Outils,
                  VerifFormat,
                  ErreurConsistance)


class Edition(object):
    """
    Classe pour l'importation des paramètres d'édition
    """

    nom_fichier = "paramedit.csv"
    libelle = "Paramètres d'Edition"
    cles = ['chemin', 'Id-Plateforme', 'année', 'mois', 'filigrane', 'chemin_filigrane']

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        donnees_csv = {}
        try:
            for ligne in dossier_source.reader(self.nom_fichier):
                cle = ligne[0]
                if cle not in self.cles:
                    Outils.fatal(ErreurConsistance(),
                                 "Clé inconnue dans %s: %s" % (self.nom_fichier, cle))
                donnees_csv[cle] = ligne[1]
        except IOError as e:
            Outils.fatal(e, "impossible d'ouvrir le fichier : "+self.nom_fichier)

        msg = ""
        for cle in self.cles:
            if cle not in donnees_csv:
                msg += "\nClé manquante dans %s: %s" % (self.nom_fichier, cle)

        self.annee, err = VerifFormat.est_un_entier(donnees_csv['année'], "l'année", mini=2000, maxi=2099)
        msg += err

        self.mois, err = VerifFormat.est_un_entier(donnees_csv['mois'], "le mois", mini=1, maxi=12)
        msg += err

        self.plateforme, err = VerifFormat.est_un_alphanumerique(donnees_csv['Id-Plateforme'], "l'id plateforme")
        msg += err

        self.filigrane, err = VerifFormat.est_un_texte(donnees_csv['filigrane'], "le filigrane", vide=True)
        msg += err

        self.chemin, err = VerifFormat.est_un_chemin(donnees_csv['chemin'], "le chemin")
        msg += err
        self.chemin_filigrane, err = VerifFormat.est_un_chemin(donnees_csv['chemin_filigrane'], "le chemin filigrane")
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

        if msg != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
