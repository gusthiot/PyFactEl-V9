from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class CategPrix(CsvImport):
    """
    Classe pour l'importation des données de Catégories Prix
    """

    nom_fichier = "categprix.csv"
    cles = ['id_classe', 'id_categorie', 'prix_unit']
    libelle = "Catégories Prix"

    def __init__(self, dossier_source, classes, categories):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param classes: classes clients importées
        :param categories: catégories importées
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        clas = []
        couples = []
        ids = []

        for donnee in self.donnees:
            info = self._test_id_coherence(donnee['id_classe'], "l'id classe client", ligne, classes)
            if info == "" and donnee['id_classe'] not in clas:
                clas.append(donnee['id_classe'])
            else:
                msg += info

            info = self._test_id_coherence(donnee['id_categorie'], "l'id catégorie", ligne, categories)
            if info == "" and donnee['id_categorie'] not in ids:
                ids.append(donnee['id_categorie'])
            else:
                msg += info

            if (donnee['id_categorie'] != "") and (donnee['id_classe'] != ""):
                couple = [donnee['id_categorie'], donnee['id_classe']]
                if couple not in couples:
                    couples.append(couple)
                else:
                    msg += "Couple id catégorie '" + donnee['id_categorie'] + "' et id classe '" + \
                           donnee['id_classe'] + "' de la ligne " + str(ligne) + " pas unique\n"

            donnee['prix_unit'], info = Format.est_un_nombre(donnee['prix_unit'], "le prix unitaire ", ligne, 2)
            msg += info

            donnees_dict[donnee['id_classe'] + donnee['id_categorie']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        for id_classe in classes.donnees.keys():
            if id_classe not in clas:
                msg += "L'id de classe '" + id_classe + "' dans les classes clients n'est pas présent dans " \
                                                         "les catégories prix\n"

        for id_cat in categories.donnees.keys():
            if id_cat not in ids:
                msg += "L'id catégorie '" + id_cat + "' dans les catégories n'est pas présent dans " \
                                                         "les catégories prix\n"
        for id_cat in ids:
            for classe in clas:
                couple = [id_cat, classe]
                if couple not in couples:
                    msg += "Couple id catégorie '" + id_cat + "' et id classe client '" + \
                           classe + "' n'existe pas\n"

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
