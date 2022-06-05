import os
import zipfile
import shutil
import errno

from core import Interface


class Chemin(object):
    """
    Classe contenant diverses méthodes liées à la création des chemins
    """

    @staticmethod
    def chemin(structure):
        """
        construit le chemin pour dossier/fichier
        :param edition: paramètres d'édition
        :return: chemin logique complet pour dossier/fichier
        """
        chemin = ""
        first = True
        for element in structure:
            if not first:
                chemin += "/"
            else:
                first = False
            chemin += str(element)
        return chemin.replace("//", "/")

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

        for client in csv_fichiers.values():
            fichier_zip = zipfile.ZipFile(chemin_destination + "/" + client['nom'], 'w')
            for file in client['fichiers']:
                fichier_zip.write(os.path.join(chemin_destination, file),
                                  os.path.relpath(os.path.join(chemin_destination, file), chemin_destination),
                                  compress_type=zipfile.ZIP_DEFLATED)
            fichier_zip.close()
            try:
                for file in client['fichiers']:
                    os.unlink(os.path.join(chemin_destination, file))
            except IOError as err:
                Interface.affiche_message("IOError: {0}".format(err))

    @staticmethod
    def copier_dossier(source, dossier, destination):
        """
        copier un dossier
        :param source: chemin du dossier à copier
        :param dossier: dossier à copier
        :param destination: chemin de destination de copie
        """
        chemin = destination + "/" + dossier
        if not os.path.exists(chemin):
            try:
                shutil.copytree(source + dossier, chemin)
            except OSError as exc:
                if exc.errno == errno.ENOTDIR:
                    shutil.copy(source, destination)
