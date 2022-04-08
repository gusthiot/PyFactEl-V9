from imports import Fichier
from core import Outils


class Granted(Fichier):
    """
    Classe pour l'importation des données de Subsides comptabilisés
    """

    cles = ['id_compte', 'id_plateforme', 'id_article', 'montant']
    libelle = "Subsides comptabilisés"

    def __init__(self, dossier_source, edition):
        if edition.mois > 1:
            self.nom_fichier = "granted_" + str(edition.annee) + "_" + Outils.mois_string(edition.mois-1) + ".csv"
        else:
            self.nom_fichier = "granted_" + str(edition.annee-1) + "_" + Outils.mois_string(12) + ".csv"
        super().__init__(dossier_source)

    def est_coherent(self, comptes, artsap, plateformes):
        """
        vérifie que les données du fichier importé sont cohérentes
        :param comptes: comptes importés
        :param artsap: articles SAP importés
        :param plateformes: plateformes importées
        :return: 1 s'il y a une erreur, 0 sinon
        """

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        msg = ""
        ligne = 1
        donnees_dict = {}
        triplets = []

        del self.donnees[0]
        for donnee in self.donnees:
            if donnee['id_compte'] == "":
                msg += "l'id compte de la ligne " + str(ligne) + " ne peut être vide\n"
            elif comptes.contient_id(donnee['id_compte']) == 0:
                msg += "l'id compte '" + donnee['id_compte'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"
            if donnee['id_article'] == "":
                msg += "l'id article SAP de la ligne " + str(ligne) + " ne peut être vide\n"
            elif not artsap.contient_id(donnee['id_article']):
                msg += "l'id article SAP de la ligne " + str(ligne) + " n'existe pas dans les codes D\n"

            if donnee['id_plateforme'] == "":
                msg += "l'id plateforme de la ligne " + str(ligne) + " ne peut être vide\n"
            elif plateformes.contient_id(donnee['id_plateforme']) == 0:
                msg += "l'id plateforme '" + donnee['id_plateforme'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            triplet = [donnee['id_compte'], donnee['id_plateforme'], donnee['id_article']]
            if triplet not in triplets:
                triplets.append(triplet)
            else:
                msg += "Triplet type '" + donnee['type'] + "' id plateforme '" + donnee['id_plateforme'] + \
                       "' et id article SAP '" + donnee['id_article'] + "' de la ligne " + str(ligne) + " pas unique\n"

            donnee['montant'], info = Outils.est_un_nombre(donnee['montant'], "le montant comptabilisé", ligne, 2, 0)
            msg += info

            donnees_dict[donnee['id_compte'] + donnee['id_plateforme'] + donnee['id_article']] = donnee
            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
