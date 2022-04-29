from core import CsvImport
from core import (Interface,
                  ErreurConsistance)


class CleSubside(CsvImport):
    """
    Classe pour l'importation des données de Subsides
    """

    nom_fichier = "clesubside.csv"
    cles = ['type', 'id_classe', 'code_client', 'id_machine']
    libelle = "Clés Subsides"

    def __init__(self, dossier_source, clients, machines, classes, subsides):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param clients: clients importés
        :param machines: machines importées
        :param classes: classes clients importées
        :param subsides: subsides importés
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        quadruplets = []

        for donnee in self.donnees:
            msg += self._test_id_coherence(donnee['type'], "le type", ligne, subsides)

            msg += self._test_id_coherence(donnee['id_classe'], "l'id classe client", ligne, classes, True)

            msg += self._test_id_coherence(donnee['code_client'], "le code client", ligne, clients, True)

            msg += self._test_id_coherence(donnee['id_machine'], "l'id machine", ligne, machines, True)

            quadruplet = donnee['type'] + donnee['id_classe'] + donnee['code_client'] + donnee['id_machine']

            if quadruplet not in quadruplets:
                quadruplets.append(quadruplet)
            else:
                msg += "le quadruplet de la ligne " + str(ligne) + \
                       " n'est pas unique\n"

            if donnee['type'] not in donnees_dict:
                donnees_dict[donnee['type']] = {}
            dict_p = donnees_dict[donnee['type']]
            if donnee['id_classe'] not in dict_p:
                dict_p[donnee['id_classe']] = {}
            dict_n = dict_p[donnee['id_classe']]
            if donnee['code_client'] not in dict_n:
                dict_n[donnee['code_client']] = {}
            dict_c = dict_n[donnee['code_client']]
            if donnee['id_machine'] not in dict_c:
                dict_c[donnee['id_machine']] = donnee

            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
