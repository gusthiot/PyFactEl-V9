from imports import Fichier
from core import Outils


class Livraison(Fichier):
    """
    Classe pour l'importation des données de Livraisons
    """

    cles = ['annee', 'mois', 'id_compte', 'id_user', 'id_prestation', 'date_livraison', 'quantite', 'rabais',
            'id_operateur', 'id_livraison', 'date_commande', 'remarque']
    nom_fichier = "lvr.csv"
    libelle = "Livraison Prestations"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def est_coherent(self, comptes, prestations, users):
        """
        vérifie que les données du fichier importé sont cohérentes, et efface les colonnes mois et année
        :param comptes: comptes importés
        :param prestations: prestations importées
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

            if donnee['id_prestation'] == "":
                msg += "le prestation id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif prestations.contient_id(donnee['id_prestation']) == 0:
                msg += "le prestation id '" + donnee['id_prestation'] + "' de la ligne " + str(ligne) +\
                       " n'est pas référencé\n"

            if donnee['id_user'] == "":
                msg += "le user id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif users.contient_id(donnee['id_user']) == 0:
                msg += "le user id '" + donnee['id_user'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            if donnee['id_operateur'] == "":
                msg += "l'id opérateur de la ligne " + str(ligne) + " ne peut être vide\n"
            elif users.contient_id(donnee['id_operateur']) == 0:
                msg += "l'id opérateur '" + donnee['id_operateur'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            donnee['quantite'], info = Outils.est_un_nombre(donnee['quantite'], "la quantité", ligne, 1, 0)
            msg += info
            donnee['rabais'], info = Outils.est_un_nombre(donnee['rabais'], "le rabais", ligne, 2, 0)
            msg += info

            donnee['date_livraison'], info = Outils.est_une_date(donnee['date_livraison'], "la date de livraison",
                                                                 ligne)
            msg += info
            donnee['date_commande'], info = Outils.est_une_date(donnee['date_commande'], "la date de commande", ligne)
            msg += info

            donnee['id_livraison'], info = Outils.est_un_texte(donnee['id_livraison'], "l'id livraison", ligne)
            msg += info
            donnee['remarque'], info = Outils.est_un_texte(donnee['remarque'], "la remarque", ligne, True)
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
