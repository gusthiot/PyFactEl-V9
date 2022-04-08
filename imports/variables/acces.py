from imports import Fichier
from core import Outils


class Acces(Fichier):
    """
    Classe pour l'importation des données de Contrôle Accès Equipement
    """

    cles = ['annee', 'mois', 'id_compte', 'id_user', 'id_machine', 'date_login', 'duree_machine_hp', 'duree_machine_hc',
            'duree_run', 'duree_operateur', 'id_op', 'remarque_op', 'remarque_staff']
    nom_fichier = "cae.csv"
    libelle = "Contrôle Accès Equipement"

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
                msg += "le compte id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif comptes.contient_id(donnee['id_compte']) == 0:
                msg += "le compte id '" + donnee['id_compte'] + "' de la ligne " + str(ligne) + " n'est pas référencé\n"
            elif donnee['id_compte'] not in coms:
                coms.append(donnee['id_compte'])

            if donnee['id_machine'] == "":
                msg += "le machine id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif machines.contient_id(donnee['id_machine']) == 0:
                msg += "le machine id '" + donnee['id_machine'] + "' de la ligne " + str(ligne)\
                       + " n'est pas référencé\n"

            if donnee['id_user'] == "":
                msg += "le user id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif users.contient_id(donnee['id_user']) == 0:
                msg += "le user id '" + donnee['id_user'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            if donnee['id_op'] == "":
                msg += "l'id opérateur de la ligne " + str(ligne) + " ne peut être vide\n"
            elif users.contient_id(donnee['id_op']) == 0:
                msg += "l'id opérateur '" + donnee['id_op'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            donnee['duree_machine_hp'], info = Outils.est_un_nombre(donnee['duree_machine_hp'], "la durée machine hp",
                                                                    ligne, 4, 0)
            msg += info
            donnee['duree_machine_hc'], info = Outils.est_un_nombre(donnee['duree_machine_hc'], "la durée machine hc",
                                                                    ligne, 4, 0)
            msg += info
            donnee['duree_run'], info = Outils.est_un_nombre(donnee['duree_run'], "la durée du run",
                                                             ligne, 4, 0)
            msg += info
            donnee['duree_operateur'], info = Outils.est_un_nombre(donnee['duree_operateur'], "la durée opérateur",
                                                                   ligne, 4, 0)
            msg += info
            if donnee['duree_run'] < (donnee['duree_machine_hc'] + donnee['duree_machine_hp']):
                msg += "la durée de run de la ligne " + str(ligne) + "ne peut pas être plus petite que HP + HC"

            donnee['date_login'], info = Outils.est_une_date(donnee['date_login'], "la date de login", ligne)
            msg += info

            donnee['remarque_op'], info = Outils.est_un_texte(donnee['remarque_op'], "la remarque opérateur", ligne,
                                                              True)
            msg += info

            donnee['remarque_staff'], info = Outils.est_un_texte(donnee['remarque_staff'], "la remarque staff", ligne,
                                                                 True)
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
