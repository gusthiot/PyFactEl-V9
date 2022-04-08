from imports import Fichier
from core import (Outils,
                  ErreurCoherence)


class Prestation(Fichier):
    """
    Classe pour l'importation des données de Prestations du catalogue
    """

    cles = ['annee', 'mois', 'id_prestation', 'no_prestation', 'designation', 'id_article', 'unite_prest', 'prix_unit',
            'id_plateforme', 'id_machine']
    nom_fichier = "prestation.csv"
    libelle = "Prestations"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contient_id(self, id_prestation):
        """
        vérifie si une prestation contient l'id donné
        :param id_prestation: id à vérifier
        :return: 1 si id contenu, 0 sinon
        """
        if self.verifie_coherence == 1:
            if id_prestation in self.donnees.keys():
                return 1
        else:
            Outils.fatal(ErreurCoherence(),
                         self.libelle + ": la consistance de " + self.nom_fichier +
                         " doit être vérifiée avant d'en utiliser les données")
        return 0

    def est_coherent(self, artsap, coefprests, plateformes, machines):
        """
        vérifie que les données du fichier importé sont cohérentes et efface les colonnes mois et année
        :param artsap: articles SAP importés
        :param coefprests: coefficients prestations importés
        :param plateformes: plateformes importées
        :param machines: machines importées
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
            donnee['id_prestation'], info = Outils.est_un_alphanumerique(donnee['id_prestation'], "l'id prestation",
                                                                         ligne)
            msg += info
            if info == "":
                if donnee['id_prestation'] not in ids:
                    ids.append(donnee['id_prestation'])
                else:
                    msg += "l'id prestation '" + donnee['id_prestation'] + "' de la ligne " + str(ligne) +\
                           " n'est pas unique\n"

            if donnee['no_prestation'] == "":
                msg += "le numéro de prestation de la ligne " + str(ligne) + " ne peut être vide\n"
            else:
                donnee['no_prestation'], info = Outils.est_un_alphanumerique(donnee['no_prestation'],
                                                                             "le no prestation", ligne)
                msg += info

            donnee['designation'], info = Outils.est_un_texte(donnee['designation'], "la désignation", ligne)
            msg += info
            donnee['unite_prest'], info = Outils.est_un_texte(donnee['unite_prest'], "l'unité prestation", ligne, True)
            msg += info

            if donnee['id_article'] == "":
                msg += "l'id article SAP  de la ligne " + str(ligne) + " ne peut être vide\n"
            elif not artsap.contient_id(donnee['id_article']):
                msg += "l'id article SAP de la ligne " + str(ligne) + " n'existe pas dans les codes D\n"
            elif coefprests.contient_article(donnee['id_article']) == 0:
                msg += "l'id article SAP' '" + donnee['id_article'] + "' de la ligne " + str(ligne) +\
                       " n'est pas référencée dans les coefficients\n"

            if donnee['id_plateforme'] == "":
                msg += "l'id plateforme de la ligne " + str(ligne) + " ne peut être vide\n"
            elif plateformes.contient_id(donnee['id_plateforme']) == 0:
                msg += "l'id plateforme '" + donnee['id_plateforme'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            if donnee['id_machine'] == "":
                msg += "l'id machine de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_machine'] != "0":
                if machines.contient_id(donnee['id_machine']) == 0:
                    msg += "l'id machine '" + donnee['id_machine'] + "' de la ligne " + str(ligne) \
                           + " n'est pas référencé ni égal à 0\n"

            donnee['prix_unit'], info = Outils.est_un_nombre(donnee['prix_unit'], "le prix unitaire", ligne, 2, 0)
            msg += info

            del donnee['annee']
            del donnee['mois']
            donnees_dict[donnee['id_prestation']] = donnee
            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
