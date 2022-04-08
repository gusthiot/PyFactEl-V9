from imports import Fichier
from core import (Outils,
                  ErreurCoherence)


class Machine(Fichier):
    """
    Classe pour l'importation des données de Machines Cmi
    """

    cles = ['annee', 'mois', 'id_machine', 'nom', 'id_groupe', 'tx_rabais_hc']
    nom_fichier = "machine.csv"
    libelle = "Machines"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contient_id(self, id_machine):
        """
        vérifie si une machine contient l'id donné
        :param id_machine: id à vérifier
        :return: 1 si id contenu, 0 sinon
        """
        if self.verifie_coherence == 1:
            if id_machine in self.donnees.keys():
                return 1
        else:
            Outils.fatal(ErreurCoherence(),
                         self.libelle + ": la consistance de " + self.nom_fichier +
                         " doit être vérifiée avant d'en utiliser les données")
        return 0

    def est_coherent(self, groupes):
        """
        vérifie que les données du fichier importé sont cohérentes, et efface les colonnes mois et année
        :param categories: catégories importées
        :return: 1 s'il y a une erreur, 0 sinon
        """

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        del self.donnees[0]
        msg = ""
        ligne = 1
        ids = []
        donnees_dict = {}

        for donnee in self.donnees:
            donnee['id_machine'], info = Outils.est_un_alphanumerique(donnee['id_machine'], "l'id machine", ligne)
            msg += info
            if info == "":
                if donnee['id_machine'] not in ids:
                    ids.append(donnee['id_machine'])
                else:
                    msg += "l'id machine '" + donnee['id_machine'] + "' de la ligne " + str(ligne) +\
                           " n'est pas unique\n"

            if donnee['id_groupe'] == "":
                msg += "l'id groupe de la ligne " + str(ligne) + " ne peut être vide\n"
            elif groupes.contient_id(donnee['id_groupe']) == 0:
                msg += "l'id groupe '" + donnee['id_groupe'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            donnee['tx_rabais_hc'], info = Outils.est_un_nombre(donnee['tx_rabais_hc'], "le rabais heures creuses",
                                                                ligne, min=0, max=100)
            msg += info
            donnee['nom'], info = Outils.est_un_texte(donnee['nom'], "le nom machine", ligne)
            msg += info

            del donnee['annee']
            del donnee['mois']
            donnees_dict[donnee['id_machine']] = donnee
            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
