from imports import Fichier
from core import Outils


class Service(Fichier):
    """
    Classe pour l'importation des données de Services
    """

    cles = ['annee', 'mois', 'id_compte', 'id_user', 'id_categorie', 'date', 'quantite', 'id_op', 'remarque_staff']
    nom_fichier = "srv.csv"
    libelle = "Services"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def est_coherent(self, comptes, categories, users):
        """
        vérifie que les données du fichier importé sont cohérentes, et efface les colonnes mois et année
        :param comptes: comptes importés
        :param categories: catégories importées
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
            if donnee['id_compte'] == "":
                msg += "le compte id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif comptes.contient_id(donnee['id_compte']) == 0:
                msg += "le compte id '" + donnee['id_compte'] + "' de la ligne " + str(ligne) + " n'est pas référencé\n"
            elif donnee['id_compte'] not in coms:
                coms.append(donnee['id_compte'])

            if donnee['id_categorie'] == "":
                msg += "l'id catégorie " + str(ligne) + " ne peut être vide\n"
            elif categories.contient_id(donnee['id_categorie']) == 0:
                msg += "l'id catégorie de la ligne " + str(ligne) + " n'existe pas dans les catégories \n"

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

            donnee['quantite'], info = Outils.est_un_nombre(donnee['quantite'], "la quantité", ligne, 3, 0)
            msg += info

            donnee['date'], info = Outils.est_une_date(donnee['date'], "la date", ligne)
            msg += info

            donnee['remarque_staff'], info = Outils.est_un_texte(donnee['remarque_staff'], "la remarque staff", ligne,
                                                                 True)
            msg += info

            del donnee['annee']
            del donnee['mois']
            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
