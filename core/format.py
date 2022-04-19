from datetime import datetime
import re


class Format(object):
    """
    Classe contenant des méthodes pour vérifier ou adapter le format des données
    """
    @staticmethod
    def mois_string(mois):
        """
        prend un mois comme nombre, et le retourne comme string, avec un '0' devant si plus petit que 10
        :param mois: mois formaté en nombre
        :return: mois formaté en string
        """
        if mois < 10:
            return "0" + str(mois)
        else:
            return str(mois)

    @staticmethod
    def est_un_texte(donnee, colonne, ligne=-1, vide=False):
        """
        vérifie que la donnée est bien un texte
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param ligne: ligne contenant la donnée (-1 si pas de ligne)
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        if ligne > -1:
            delaligne = " de la ligne " + str(ligne)
        else:
            delaligne = ""
        try:
            s_d = str(donnee)
            if s_d.startswith('"') and s_d.endswith('"'):
                s_d = s_d[1:-1]
            if s_d == "" and not vide:
                return "", colonne + delaligne + " ne peut être vide\n"
            return s_d, ""
        except ValueError:
            return "", colonne + delaligne + " doit être un texte\n"

    @staticmethod
    def est_une_date(donnee, colonne, ligne=-1, vide=False):
        """
        vérifie que la donnée est bien une date
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param ligne: ligne contenant la donnée (-1 si pas de ligne)
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        if ligne > -1:
            delaligne = " de la ligne " + str(ligne)
        else:
            delaligne = ""
        try:
            s_d = str(donnee)
            if s_d.startswith('"') and s_d.endswith('"'):
                s_d = s_d[1:-1]
            if s_d == "":
                if not vide:
                    return "", colonne + delaligne + " ne peut être vide\n"
                else:
                    return "", ""
            date = datetime.strptime(s_d, '%Y-%m-%d %H:%M:%S')
            return date, ""
        except ValueError:
            return "", colonne + delaligne + " doit être une date du bon format : YYYY-MM-DD HH:MM:SS\n"

    @staticmethod
    def est_un_document(donnee, colonne, ligne=-1, vide=False):
        """
        vérifie que la donnée est bien un nom de document
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param ligne: ligne contenant la donnée (-1 si pas de ligne)
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        if ligne > -1:
            delaligne = " de la ligne " + str(ligne)
        else:
            delaligne = ""
        try:
            chars = set('\/:*?“<>|')
            s_d = str(donnee)
            if s_d == "" and not vide:
                return "", colonne + delaligne + " ne peut être vide\n"
            if any((c in chars) for c in s_d):
                return "", colonne + delaligne + " n'est pas un nom de document valide\n"
            return s_d, ""
        except:
            return "", colonne + delaligne + " doit être un texte\n"

    @staticmethod
    def est_un_chemin(donnee, colonne, ligne=-1, vide=False):
        """
        vérifie que la donnée est bien un chemin
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param ligne: ligne contenant la donnée (-1 si pas de ligne)
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        if ligne > -1:
            delaligne = " de la ligne " + str(ligne)
        else:
            delaligne = ""
        try:
            chars = set('*?"<>|')
            s_d = str(donnee)
            if s_d == "" and not vide:
                return "", colonne + delaligne + " ne peut être vide\n"
            if any((c in chars) for c in s_d):
                return "", colonne + delaligne + " n'est pas un chemin valide\n"
            return s_d, ""
        except:
            return "", colonne + delaligne + " doit être un texte\n"

    @staticmethod
    def est_un_alphanumerique(donnee, colonne, ligne=-1, barres=False, chevrons=False, vide=False):
        """
        vérifie que la donnée est bien un texte
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param ligne: ligne contenant la donnée (-1 si pas de ligne)
        :param barres: True si la variable peut contenir des barres obliques, False sinon
        :param chevrons: True si la variable peut contenir des < >, False sinon
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        if ligne > -1:
            delaligne = " de la ligne " + str(ligne)
        else:
            delaligne = ""
        try:
            if barres:
                if chevrons:
                    pattern = '^[a-zA-Z0-9_<>\-./\\\\]+$'
                else:
                    pattern = '^[a-zA-Z0-9_\-./\\\\]+$'
            else:
                if chevrons:
                    pattern = '^[a-zA-Z0-9_<>\-]+$'
                else:
                    pattern = '^[a-zA-Z0-9_\-]+$'
            s_d = str(donnee)
            if s_d == "":
                if not vide:
                    return "", colonne + delaligne + " ne peut être vide\n"
                else:
                    return "", ""
            if not re.match(pattern, s_d):
                return "", colonne + delaligne + " n'est pas un alphanumérique valide\n"
            return s_d, ""
        except:
            return "", colonne + delaligne + " doit être un texte\n"

    @staticmethod
    def est_un_nombre(donnee, colonne, ligne=-1, arrondi=-1, mini=None, maxi=None):
        """
        vérifie que la donnée est bien un nombre
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param ligne: ligne contenant la donnée (-1 si pas de ligne)
        :param arrondi: arrondi après la virgule (-1 si pas d'arrondi)
        :param mini: borne minimale facultative
        :param maxi: borne maximale facultative
        :return: la donnée formatée en nombre et un string vide si ok, 0 et un message d'erreur sinon
        """
        if ligne > -1:
            delaligne = " de la ligne " + str(ligne)
        else:
            delaligne = ""
        try:
            fl_d = float(donnee)
            if mini is not None and fl_d < mini:
                return -1, colonne + delaligne + " doit être un nombre >= " + str(min) + "\n"
            if maxi is not None and fl_d > maxi:
                return -1, colonne + delaligne + " doit être un nombre <= " + str(max) + "\n"
            if arrondi > -1:
                return round(fl_d, arrondi), ""
            else:
                return fl_d, ""
        except ValueError:
            return -1, colonne + delaligne + " doit être un nombre\n"

    @staticmethod
    def est_un_entier(donnee, colonne, ligne=-1, mini=None, maxi=None):
        """
        vérifie que la donnée est bien un nombre entier dans les bornes éventuelles
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param ligne: ligne contenant la donnée (-1 si pas de ligne)
        :param mini: borne minimale facultative
        :param maxi: borne maximale facultative
        :return: la donnée formatée en nombre et un string vide si ok, 0 et un message d'erreur sinon
        """
        if ligne > -1:
            delaligne = " de la ligne " + str(ligne)
        else:
            delaligne = ""
        try:
            entier = int(donnee)
            if mini is not None and entier < mini:
                return -1, colonne + delaligne + " doit être un nombre entier >= " + str(min) + "\n"
            if maxi is not None and entier > maxi:
                return -1, colonne + delaligne + " doit être un nombre entier <= " + str(max) + "\n"
            return entier, ""
        except ValueError:
            return -1, colonne + delaligne + " doit être un nombre entier\n"
