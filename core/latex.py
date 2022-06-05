import re
import os
import shutil
import sys
import subprocess
from core import Interface


class Latex(object):

    @classmethod
    def possibles(cls):
        return bool(shutil.which("pdflatex"))

    @staticmethod
    def echappe_caracteres(texte):
        """
        échappement des caractères qui peuvent poser problème dans les tableaux latex
        :param texte: texte à échapper
        :return: texte échappé
        """

        p = re.compile("[^ a-zA-Z0-9_'Éèéêëâàäïûùüçöô.:,;+<>\-%#&@\\\\$/|()\[\]\{\}]")
        texte = p.sub('', texte)

        texte = texte.replace('\\', '\\textbackslash')
        caracteres = ['%', '$', '_', '&', '#', '{', '}']
        latex_c = ['\%', '\$', '\_', '\&', '\#', '\{', '\}']
        for pos in range(0, len(caracteres)):
            texte = texte.replace(caracteres[pos], latex_c[pos])

        return texte

    @staticmethod
    def creer_latex_pdf(nom_fichier, contenu):
        """
        création d'un pdf à partir d'un contenu latex
        :param nom_fichier: nom du pdf final
        :param contenu: contenu latex
        """
        with open(nom_fichier + ".tex", 'w') as f:
            f.write(contenu)

        proc = subprocess.Popen(['pdflatex', nom_fichier + ".tex"])
        proc.communicate()

        # 2 fois pour que les longtable soient réguliers (courant de relancer latex)

        proc = subprocess.Popen(['pdflatex', nom_fichier + ".tex"])
        proc.communicate()

        try:
            os.unlink(nom_fichier + '.tex')
            os.unlink(nom_fichier + '.log')
            os.unlink(nom_fichier + '.aux')

        except IOError as err:
            Interface.affiche_message("IOError: {0}".format(err))

    @staticmethod
    def finaliser_pdf(nom_fichier, chemin_dossier=""):
        """
        déplacer le pdf créé si nécessaire
        :param nom_fichier: nom du pdf
        :param chemin_dossier: chemin du dossier dans lequel enregistrer le pdf
        """
        fichier = nom_fichier + ".pdf"
        try:
            if chemin_dossier != '':
                shutil.copy(fichier, chemin_dossier)
                os.unlink(fichier)
        except IOError as err:
            Interface.affiche_message("IOError: {0}".format(err))

    @staticmethod
    def entete():
        """
        création de l'entête de fichier latex en fonction de l'OS
        :return: le contenu de l'entête
        """
        debut = r'''\documentclass[a4paper,10pt]{article}
            \usepackage{geometry}
            \geometry{
             left=13mm,
             right=13mm,
             top=15mm,
             bottom=15mm,
             includefoot
            }
            \usepackage{lmodern}
            \usepackage[T1]{fontenc}
            \usepackage[french]{babel}
            \usepackage{microtype}
            \DisableLigatures{encoding = *, family = * }
            
            \usepackage{helvet}
            \renewcommand{\familydefault}{\sfdefault}
            '''
        if sys.platform == "win32":
            debut += r'''
                \usepackage[cp1252]{inputenc}
                '''
        elif sys.platform == "darwin":
            debut += r'''\usepackage[appelmac]{inputenc}'''
        else:
            debut += r'''\usepackage[utf8]{inputenc}'''
        return debut
