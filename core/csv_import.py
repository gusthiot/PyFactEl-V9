from core import (Interface,
                  ErreurConsistance)


class CsvImport(object):
    """
    Classe de base des classes d'importation de données

    Attributs de classe (à définir dans les sous-classes) :
         nom_fichier    Le nom relatif du fichier à charger
         libelle        Un intitulé pour les messages d'erreur
         cles           La liste des colonnes à charger
    """
    nom_fichier = ""
    cles = []
    libelle = ""

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        try:
            fichier_reader = dossier_source.reader(self.nom_fichier)
            donnees_csv = []
            for ligne in fichier_reader:
                donnees_ligne = self._extraction_ligne(ligne)
                if donnees_ligne == -1:
                    continue
                donnees_csv.append(donnees_ligne)
            self.donnees = donnees_csv
        except IOError as e:
            Interface.fatal(e, "impossible d'ouvrir le fichier : "+self.nom_fichier)

    def _extraction_ligne(self, ligne):
        """
        extracte une ligne de données du csv
        :param ligne: ligne lue du fichier
        :return: tableau représentant la ligne, indexé par les clés
        """
        num = len(self.cles)
        if len(ligne) != num:
            Interface.fatal(ErreurConsistance(),
                         self.libelle + ": nombre de lignes incorrect : " +
                         str(len(ligne)) + ", attendu : " + str(num))
        donnees_ligne = {}
        for xx in range(0, num):
            donnees_ligne[self.cles[xx]] = ligne[xx]
        return donnees_ligne

    @staticmethod
    def _test_id_coherence(donnee, nom, ligne, corpus, zero=False):
        msg = ""
        if donnee == "":
            msg += nom + " de la ligne " + str(ligne) + " ne peut être vide\n"
        elif (not zero or donnee != "0") and donnee not in corpus.donnees.keys():
            msg += nom + " '" + donnee + "' de la ligne " + str(ligne) + " n'est pas référencé"
            if zero:
                msg += " ni égal à 0"
            msg += "\n"
        return msg
