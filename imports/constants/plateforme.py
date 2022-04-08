from imports import Fichier
from core import (Outils,
                  ErreurCoherence)


class Plateforme(Fichier):
    """
    Classe pour l'importation des données de Plateformes
    """

    nom_fichier = "plateforme.csv"
    cles = ['id_plateforme', 'code_p', 'centre', 'fonds', 'abrev_plat', 'int_plat', 'grille']
    libelle = "Plateformes"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids = []

    def contient_id(self, id_plat):
        """
        vérifie si une plateforme contient l'id donné
        :param id_plat: id à vérifier
        :return: 1 si id contenu, 0 sinon
        """
        if self.verifie_coherence == 1:
            if id_plat in self.donnees.keys():
                return 1
        else:
            Outils.fatal(ErreurCoherence(),
                         self.libelle + ": la consistance de " + self.nom_fichier +
                         " doit être vérifiée avant d'en utiliser les données")
        return 0

    def est_coherent(self, clients, dossier_source):
        """
        vérifie que les données du fichier importé sont cohérentes
        :param clients: clients importés
        :param dossier_source: dossier contenant les fichiers d'entrée
        :return: 1 s'il y a une erreur, 0 sinon
        """

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        msg = ""
        ligne = 1
        donnees_dict = {}
        abrevs = []

        del self.donnees[0]
        for donnee in self.donnees:
            if donnee['id_plateforme'] == "":
                msg += "l'id plateforme " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_plateforme'] not in clients.obtenir_codes():
                msg += "l'id plateforme de la ligne " + str(ligne) + " n'existe pas dans les clients \n"
            elif donnee['id_plateforme'] not in self.ids:
                self.ids.append(donnee['id_plateforme'])
            else:
                msg += "l'id plateforme de la ligne " + str(ligne) + " n'est pas unique \n"
            donnee['code_p'], info = Outils.est_un_alphanumerique(donnee['code_p'], "le code P", ligne)
            msg += info
            donnee['centre'], info = Outils.est_un_alphanumerique(donnee['centre'], "le centre financier", ligne)
            msg += info
            donnee['fonds'], info = Outils.est_un_alphanumerique(donnee['fonds'], "les fonds à créditer", ligne)
            msg += info
            donnee['abrev_plat'], info = Outils.est_un_alphanumerique(donnee['abrev_plat'], "l'abréviation", ligne)
            msg += info
            if donnee['abrev_plat'] not in abrevs:
                abrevs.append(donnee['abrev_plat'])
            else:
                msg += "l'abréviation plateforme de la ligne " + str(ligne) + " n'est pas unique \n"
            donnee['int_plat'], info = Outils.est_un_texte(donnee['int_plat'], "l'intitulé", ligne)
            msg += info
            donnee['grille'], info = Outils.est_un_document(donnee['grille'], "la grille tarifaire", ligne, True)
            msg += info
            if donnee['grille'] != "":
                if not Outils.existe(Outils.chemin([dossier_source.chemin, donnee['grille'] + '.pdf'])):
                    msg += "la grille de la ligne " + str(ligne) + " n'existe pas dans le dossier d'entrée \n"

            donnees_dict[donnee['id_plateforme']] = donnee
            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            Outils.affiche_message(msg)
            return 1
        return 0
