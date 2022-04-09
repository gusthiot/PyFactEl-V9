from imports import Fichier
from core import Outils


class NoShow(Fichier):
    """
    Classe pour l'importation des données de No Show
    """

    cles = ['annee', 'mois', 'date_debut', 'type', 'id_machine', 'id_user', 'id_compte', 'penalite']
    nom_fichier = "noshow.csv"
    libelle = "Pénalités No Show"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def est_coherent(self, comptes, machines, users):
        """
        vérifie que les données du fichier importé sont cohérentes, et efface les colonnes mois et année
        :param comptes: comptes importés
        :param machines: machines importées
        :param users: users importés
        :return: 1 s'il y a une erreur, 0 sinon
        """
        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_list = []
        coms = []

        for donnee in self.donnees:
            donnee['mois'], info = Outils.est_un_entier(donnee['mois'], "le mois ", ligne, 1, 12)
            msg += info
            donnee['annee'], info = Outils.est_un_entier(donnee['annee'], "l'annee ", ligne, 2000, 2099)
            msg += info

            if donnee['id_compte'] == "":
                msg += "le id compte de la ligne " + str(ligne) + " ne peut être vide\n"
            elif comptes.contient_id(donnee['id_compte']) == 0:
                msg += "le id compte '" + donnee['id_compte'] + "' de la ligne " + str(ligne) + " n'est pas référencé\n"
            elif donnee['id_compte'] not in coms:
                coms.append(donnee['id_compte'])

            if donnee['id_machine'] == "":
                msg += "le machine id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif machines.contient_id(donnee['id_machine']) == 0:
                msg += "le machine id '" + donnee['id_machine'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            if donnee['id_user'] == "":
                msg += "le user id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif users.contient_id(donnee['id_user']) == 0:
                msg += "le user id '" + donnee['id_user'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            if donnee['type'] == "":
                msg += "HP/HC " + str(ligne) + " ne peut être vide\n"
            elif donnee['type'] != "HP" and donnee['type'] != "HC":
                msg += "HP/HC " + str(ligne) + " doit être égal à HP ou HC\n"

            donnee['penalite'], info = Outils.est_un_nombre(donnee['penalite'], "la pénalité", ligne, 2, 0)
            msg += info

            donnee['date_debut'], info = Outils.est_une_date(donnee['date_debut'], "la date de début", ligne)
            msg += info

            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
