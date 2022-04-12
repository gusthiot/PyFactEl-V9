from imports import Edition
from imports.constants import (ArticleSap,
                               Categorie,
                               CategPrix,
                               ClasseClient,
                               CoefPrest,
                               Generaux,
                               Granted,
                               Groupe,
                               Machine,
                               Paramtexte,
                               Plateforme,
                               Prestation,
                               UserLabo)
from imports.variables import (Acces,
                               CleSubside,
                               Client,
                               Compte,
                               Livraison,
                               NoShow,
                               PlafSubside,
                               Service,
                               Subside,
                               User)
from core import (Outils, ErreurConsistance, DossierSource)


class ImportD(object):
    """
    Classe pour l'importation des données nécessaires au module D
    """

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """

        self.paramtexte = Paramtexte(dossier_source)
        self.generaux = Generaux(dossier_source)
        self.classes = ClasseClient(dossier_source)
        self.clients = Client(dossier_source, self.generaux, self.classes)
        self.plateformes = Plateforme(dossier_source, self.clients)
        self.artsap = ArticleSap(dossier_source)
        self.edition = Edition(dossier_source, self.plateformes)
        self.categories = Categorie(dossier_source, self.artsap, self.plateformes)
        self.groupes = Groupe(dossier_source, self.categories)
        self.machines = Machine(dossier_source, self.groupes, self.edition)
        self.subsides = Subside(dossier_source)
        self.plafonds = PlafSubside(dossier_source, self.subsides, self.artsap, self.plateformes)
        self.cles = CleSubside(dossier_source, self.clients, self.machines, self.classes, self.subsides)
        self.comptes = Compte(dossier_source, self.clients, self.subsides)
        self.users = User(dossier_source)
        self.categprix = CategPrix(dossier_source, self.classes, self.categories)
        self.coefprests = CoefPrest(dossier_source, self.classes, self.artsap)
        self.prestations = Prestation(dossier_source, self.artsap, self.coefprests, self.plateformes, self.machines,
                                      self.edition)

        self.plateforme = self.plateformes.donnees[self.edition.plateforme]

        if self.edition.filigrane != "":
            chemin = self.generaux.chemin_filigrane
        else:
            chemin = self.generaux.chemin
        self.dossier_enregistrement = Outils.chemin([chemin, self.plateforme['abrev_plat'], self.edition.annee,
                                                     Outils.mois_string(self.edition.mois)], self.generaux)

        Outils.existe(self.dossier_enregistrement, True)
        self.acces = Acces(dossier_source, self.comptes, self.machines, self.users)
        self.noshows = NoShow(dossier_source, self.comptes, self.machines, self.users)
        self.livraisons = Livraison(dossier_source, self.comptes, self.prestations, self.users)
        self.services = Service(dossier_source, self.comptes, self.categories, self.users)

        self.dossier_source = dossier_source

        if self.edition.mois > 1:
            annee_p = self.edition.annee
            mois_p = Outils.mois_string(self.edition.mois-1)
        else:
            annee_p = self.edition.annee-1
            mois_p = 12
        self.dossier_precedent = Outils.chemin([self.generaux.chemin, self.plateforme['abrev_plat'], annee_p, mois_p, "V0",
                                                "OUT"], self.generaux)
        if not Outils.existe(self.dossier_precedent, False):
            Outils.fatal(ErreurConsistance(), "le dossier " + self.dossier_precedent + " se doit d'être présent !")

        self.grants = Granted(DossierSource(self.dossier_precedent), self.edition, self.comptes, self.artsap,
                              self.plateformes)
        self.userlabs = UserLabo(DossierSource(self.dossier_precedent), self.edition, self.plateformes, self.clients,
                                 self.users)

    def copie_fixes(self, dossier_destination):
        """
        copie des fichiers fixes de base vers la destination de sauvegarde
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """
        for fichier in [self.paramtexte, self.generaux, self.classes, self.plateformes, self.artsap, self.categories,
                        self.groupes, self.machines, self.categprix, self.coefprests, self.prestations]:
            dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
        for fichier in [self.grants,
                        self.userlabs]:
            dossier_destination.ecrire(fichier.nom_fichier,
                                       DossierSource(self.dossier_precedent).lire(fichier.nom_fichier))

    def copie_variables(self, dossier_destination):
        """
        copie des fichiers variables de base vers la destination de sauvegarde
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """
        for fichier in [self.clients, self.subsides, self.plafonds, self.cles, self.comptes, self.users,
                        self.acces, self.noshows, self.livraisons, self.services]:
            dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
