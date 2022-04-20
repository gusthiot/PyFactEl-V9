

class _CsvBase(object):
    """
    Classe de base pour les fichiers csv récapitulatifs
    """
    cles = []
    nom = ""

    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        self.imports = imports


class CsvDict(_CsvBase):
    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        super().__init__(imports)
        self.valeurs = {}

    def csv(self, dossier_destination):
        """
        création du fichier csv à partir de la liste des noms de colonnes et d'un dictionnaire de valeurs
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """
        pt = self.imports.paramtexte.donnees

        with dossier_destination.writer(self.nom) as fichier_writer:
            ligne = []
            for cle in self.cles:
                ligne.append(pt[cle])
            fichier_writer.writerow(ligne)

            for valeur in self.valeurs.values():
                ligne = []
                for i in range(0, len(self.cles)):
                    ligne.append(valeur[self.cles[i]])
                fichier_writer.writerow(ligne)

    def _ajouter_valeur(self, donnee, unique):
        """
        ajout d'une ligne au prototype de csv
        :param donnee: contenu de la ligne
        :param unique: clé d'identification unique de la ligne
        """
        valeur = {}
        for i in range(0, len(self.cles)):
            valeur[self.cles[i]] = donnee[i]
        self.valeurs[unique] = valeur


class CsvList(_CsvBase):
    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        super().__init__(imports)
        self.lignes = []

    def csv(self, dossier_destination):
        """
        création du fichier csv à partir de la liste des noms de colonnes et d'une liste de valeurs
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """
        pt = self.imports.paramtexte.donnees

        with dossier_destination.writer(self.nom) as fichier_writer:
            ligne = []
            for cle in self.cles:
                ligne.append(pt[cle])
            fichier_writer.writerow(ligne)

            for ligne in self.lignes:
                fichier_writer.writerow(ligne)
