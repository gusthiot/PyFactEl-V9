

class CsvBase(object):
    """
    Classe de base pour les fichiers csv récapitulatifs
    """

    def __init__(self, imports):
        """
        initialisation des données et stockage des paramètres d'édition
        :param imports: données importées
        """
        self.imports = imports
        self.valeurs = {}

    def csv(self, dossier_destination):
        """
        création du fichier csv à partir de la liste des noms de colonnes
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """
        pt = self.imports.paramtexte.donnees

        with dossier_destination.writer(self.nom) as fichier_writer:
            ligne = []
            for cle in self.cles:
                ligne.append(pt[cle])
            fichier_writer.writerow(ligne)

            for key in self.valeurs.keys():
                valeur = self.valeurs[key]
                ligne = [self.imports.edition.annee, self.imports.edition.mois]
                for i in range(2, len(self.cles)):
                    ligne.append(valeur[self.cles[i]])
                fichier_writer.writerow(ligne)

    def ajouter_valeur(self, donnee, unique):
        """
        ajout d'une ligne au prototype de csv
        :param donnee: contenu de la ligne
        :param unique: clé d'identification unique de la ligne
        """
        valeur = {}
        for i in range(0, len(donnee)):
            valeur[self.cles[i + 2]] = donnee[i]
        self.valeurs[unique] = valeur
