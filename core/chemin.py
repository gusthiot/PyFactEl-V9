import os
import zipfile

from core import Interface


class Chemin(object):
    """
    Classe contenant diverses méthodes liées à la création des chemins
    """

    @staticmethod
    def separateur_lien(texte, facturation):
        """
        remplace le séparateur de chemin logique en fonction du lien donné dans les paramètres de facturation
        :param texte: texte à traiter
        :param facturation: paramètres de facturation
        :return: séparateur, string
        """
        if "\\" in facturation.lien:
            if "/" in facturation.lien:
                Interface.affiche_message("'/' et '\\' présents dans le lien des paramètres de facturation !!! ")
            texte = texte.replace("/", "\\")
        else:
            texte = texte.replace("\\", "/")
        return texte.replace("//", "/").replace("\\" + "\\", "\\")

    @staticmethod
    def separateur_dossier(texte, edition):
        """
        remplace le séparateur de chemin logique en fonction du chemin donné dans les paramètres d'édition
        :param texte: texte à traiter
        :param edition: paramètres d'édition
        :return: séparateur, string
        """
        if "\\" in edition.chemin:
            if "/" in edition.chemin or "/" in edition.chemin_filigrane:
                Interface.affiche_message("'/' et '\\' présents dans les chemins d'enregistrement' !!! ")
            texte = texte.replace("/", "\\")
            """
            if "\\" != Chemin.separateur_os():
                Interface.affiche_message_conditionnel("Le chemin d'enregistrement n'utilise pas le même séparateur que"
                                                    " l'os sur lequel tourne le logiciel. Voulez-vous tout de même "
                                                    "continuer ?")
            """
        else:
            texte = texte.replace("\\", "/")
            """
            if "/" != Chemin.separateur_os():
                Interface.affiche_message_conditionnel("Le chemin d'enregistrement n'utilise pas le même séparateur que"
                                                    " l'os sur lequel tourne le logiciel. Voulez-vous tout de même "
                                                    "continuer ?")
            """
        return texte.replace("//", "/").replace("\\" + "\\", "\\")

    @staticmethod
    def eliminer_double_separateur(texte):
        """
        élimine les doubles (back)slashs
        :param texte: texte à nettoyer
        :return: texte nettoyé
        """
        return texte.replace("//", "/").replace("\\" + "\\", "\\")

    @staticmethod
    def chemin(structure, edition=None):
        """
        construit le chemin pour dossier/fichier
        :param structure: éléments du chemin
        :param edition: paramètres d'édition
        :return: chemin logique complet pour dossier/fichier
        """
        chemin = ""
        first = True
        for element in structure:
            if not first:
                chemin += Interface.separateur_os()
            else:
                first = False
            chemin += str(element)
        if edition is None:
            return Chemin.eliminer_double_separateur(chemin)
        else:
            return Chemin.eliminer_double_separateur(Chemin.separateur_dossier(chemin, edition))

    @staticmethod
    def existe(chemin, creation=False):
        """
        vérifie si le dossier/fichier existe
        :param chemin: chemin du dossier/fichier
        :param creation: création de l'objet s'il n'existe pas
        :return: True si le dossier/fichier existe, False sinon
        """
        existe = True
        if not os.path.exists(chemin):
            existe = False
            if creation:
                os.makedirs(chemin)
        return existe

    @staticmethod
    def csv_files_in_zip(csv_fichiers, chemin_destination):
        """
        créer une archive zip contenant les fichiers csv d'un client et efface ensuite les fichiers csv
        :param csv_fichiers: fichiers csv et nom du fichier zip par client
        :param chemin_destination: dossier de sauvegarde des fichiers csv et du zip
        """

        for code in csv_fichiers.keys():

            fichier_zip = zipfile.ZipFile(chemin_destination + "/" + csv_fichiers[code]['nom'], 'w')
            for file in csv_fichiers[code]['fichiers']:
                fichier_zip.write(os.path.join(chemin_destination, file),
                                  os.path.relpath(os.path.join(chemin_destination, file), chemin_destination),
                                  compress_type=zipfile.ZIP_DEFLATED)
            fichier_zip.close()
            try:
                for file in csv_fichiers[code]['fichiers']:
                    os.unlink(os.path.join(chemin_destination, file))
            except IOError as err:
                Interface.affiche_message("IOError: {0}".format(err))
