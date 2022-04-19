from imports import Fichier
from core import (Interface,
                  Format,
                  ErreurConsistance)


class CoefPrest(Fichier):
    """
    Classe pour l'importation des données de Coefficients Prestations
    """

    cles = ['id_classe', 'id_article', 'coefficient']
    nom_fichier = "coeffprestation.csv"
    libelle = "Coefficients Prestations"

    def __init__(self, dossier_source, classes, artsap):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param classes: classes clients importées
        :param artsap: articles SAP importés
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        articles = []
        couples = []
        clas = []

        for donnee in self.donnees:
            info = self._test_id_coherence(donnee['id_classe'], "l'id classe client", ligne, classes)
            if info == "" and donnee['id_classe'] not in clas:
                clas.append(donnee['id_classe'])
            else:
                msg += info

            info = self._test_id_coherence(donnee['id_article'], "l'id article SAP", ligne, artsap)
            if info == "" and donnee['id_article'] not in articles:
                articles.append(donnee['id_article'])
            else:
                msg += info

            couple = [donnee['id_article'], donnee['id_classe']]
            if couple not in couples:
                couples.append(couple)
            else:
                msg += "Couple id article SAP '" + donnee['id_article'] + "' et id classe client '" + \
                       donnee['id_classe'] + "' de la ligne " + str(ligne) + " pas unique\n"

            donnee['coefficient'], info = Format.est_un_nombre(donnee['coefficient'], "le coefficient", ligne, 2, 0)
            msg += info

            donnees_dict[donnee['id_classe'] + donnee['id_article']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        for id_article in artsap.ids_d3:
            if id_article not in articles:
                msg += "L'id article SAP D3 '" + id_article + "' n'est pas présent dans "\
                                                         "les coefficients de prestations\n"

        for id_classe in classes.donnees.keys():
            if id_classe not in clas:
                msg += "L'id de classe '" + id_classe + "' dans les classes clients n'est pas présent dans " \
                                                         "les coefficients de prestations\n"

        for id_article in articles:
            for id_classe in clas:
                couple = [id_article, id_classe]
                if couple not in couples:
                    msg += "Couple id article SAP '" + id_article + "' et id classe client '" + \
                           id_classe + "' n'existe pas\n"

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)

    def contient_article(self, id_article):
        """
        vérifie si l'id de l'article SAP est présent
        :param id_article: l'id article à vérifier
        :return: True si présente, False sinon
        """
        for cle, coefprest in self.donnees.items():
            if coefprest['id_article'] == id_article:
                return True
        return False
