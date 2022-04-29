from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Groupe(CsvImport):
    """
    Classe pour l'importation des données de Machines Cmi
    """

    # K1, K2, K3, K4, K5, K5, K6
    cles = ['id_groupe', 'id_cat_mach', 'id_cat_mo', 'id_cat_plat', 'id_cat_cher', 'id_cat_hp', 'id_cat_hc',
            'id_cat_fixe']
    nom_fichier = "groupe.csv"
    libelle = "Groupes de machines"

    def __init__(self, dossier_source, categories):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param categories: catégories importées
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_groupe'], info = Format.est_un_alphanumerique(donnee['id_groupe'], "l'id groupe", ligne)
            msg += info
            if info == "":
                if donnee['id_groupe'] not in ids:
                    ids.append(donnee['id_groupe'])
                else:
                    msg += "l'id groupe '" + donnee['id_groupe'] + "' de la ligne " + str(ligne) + " n'est pas unique\n"

            cats = ['id_cat_mach', 'id_cat_mo', 'id_cat_plat', 'id_cat_cher', 'id_cat_hp', 'id_cat_hc', 'id_cat_fixe']
            noms = ['machine', 'opérateur', 'plateforme', 'onéreux', 'hp', 'hc', 'fixe']
            for ii in range(0, len(cats)):
                cat = cats[ii]
                nom = noms[ii]
                msg += self._test_id_coherence(donnee[cat], "l'id catégorie " + nom, ligne, categories, True)

            donnees_dict[donnee['id_groupe']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
