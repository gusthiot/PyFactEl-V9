from core import (Outils,
                  VerifFormat,
                  ErreurConsistance)


class Facturation(object):
    """
    Classe pour l'importation des paramètres de facturation
    """

    nom_fichier = "paramfact.csv"
    libelle = "Paramètres Généraux"
    cles = ['origine', 'code_int', 'code_ext', 'commerciale', 'canal', 'secteur', 'devise', 'lien', 'modes']

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        donnees_csv = {}
        try:
            for ligne in dossier_source.reader(self.nom_fichier):
                cle = ligne.pop(0)
                if cle not in self.cles:
                    Outils.fatal(ErreurConsistance(),
                                 "Clé inconnue dans %s: %s" % (self.nom_fichier, cle))
                while ligne[-1] == "":
                    del ligne[-1]
                donnees_csv[cle] = ligne
        except IOError as e:
            Outils.fatal(e, "impossible d'ouvrir le fichier : "+self.nom_fichier)

        msg = ""
        for cle in self.cles:
            if cle not in donnees_csv:
                msg += "\nClé manquante dans %s: %s" % (self.nom_fichier, cle)

        self.origine, err = VerifFormat.est_un_alphanumerique(donnees_csv['origine'][1], "l'origine")
        msg += err
        self.code_int, err = VerifFormat.est_un_alphanumerique(donnees_csv['code_int'][1], "le code INT")
        msg += err
        self.code_ext, err = VerifFormat.est_un_alphanumerique(donnees_csv['code_ext'][1], "le code EXT")
        msg += err
        self.commerciale, err = VerifFormat.est_un_alphanumerique(donnees_csv['commerciale'][1], "le com.")
        msg += err
        self.canal, err = VerifFormat.est_un_alphanumerique(donnees_csv['canal'][1], "le canal")
        msg += err
        self.secteur, err = VerifFormat.est_un_alphanumerique(donnees_csv['secteur'][1], "le secteur")
        msg += err
        self.devise, err = VerifFormat.est_un_alphanumerique(donnees_csv['devise'][1], "la devise")
        msg += err
        self.lien, err = VerifFormat.est_un_chemin(donnees_csv['lien'][1], "le lien")
        msg += err

        self.modes = []
        for mode in donnees_csv['modes'][1:]:
            mode, err = VerifFormat.est_un_alphanumerique(mode, "le mode d'envoi", vide=True)
            self.modes.append(mode)
            msg += err

        if msg != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
