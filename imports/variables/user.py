from imports import Fichier
from core import (Outils,
                  ErreurCoherence)


class User(Fichier):
    """
    Classe pour l'importation des données de Users
    """

    cles = ['id_user', 'sciper', 'nom', 'prenom']
    nom_fichier = "user.csv"
    libelle = "Users"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contient_id(self, id_user):
        """
        vérifie si un user contient l'id donné
        :param id_user: id à vérifier
        :return: 1 si id contenu, 0 sinon
        """
        ligne = 1
        if self.verifie_coherence == 1:
            for cle, user in self.donnees.items():
                if user['id_user'] == id_user:
                    return ligne
                ligne += 1
        else:
            Outils.fatal(ErreurCoherence(),
                         self.libelle + ": la consistance de " + self.nom_fichier +
                         " doit être vérifiée avant d'en utiliser les données")
        return 0

    def est_coherent(self):
        """
        vérifie que les données du fichier importé sont cohérentes, et efface les colonnes mois et année
        :return: 1 s'il y a une erreur, 0 sinon
        """
        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []
        # scipers = []

        for donnee in self.donnees:
            donnee['id_user'], info = Outils.est_un_alphanumerique(donnee['id_user'], "l'id user", ligne)
            msg += info
            if donnee['id_user'] == "":
                msg += "l'id user de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_user'] not in ids:
                ids.append(donnee['id_user'])
            else:
                msg += "l'id user '" + donnee['id_user'] + "' de la ligne " + str(ligne) +\
                       " n'est pas unique\n"

            donnee['sciper'], info = Outils.est_un_alphanumerique(donnee['sciper'], "le sciper", ligne)
            msg += info
            # if donnee['sciper'] == "":
            #     msg += "le sciper de la ligne " + str(ligne) + " ne peut être vide\n"
            # elif donnee['sciper'] not in scipers:
            #     scipers.append(donnee['sciper'])
            # else:
            #     msg += "le sciper '" + donnee['sciper'] + "' de la ligne " + str(ligne) +\
            #            " n'est pas unique\n"

            donnee['nom'], info = Outils.est_un_texte(donnee['nom'], "le nom", ligne)
            msg += info
            donnee['prenom'], info = Outils.est_un_texte(donnee['prenom'], "le prénom", ligne)
            msg += info

            donnees_dict[donnee['id_user']] = donnee
            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
