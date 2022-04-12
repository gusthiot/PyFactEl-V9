from imports import Edition
from imports.constants import (ArticleSap,
                               Categorie,
                               CategPrix,
                               ClasseClient,
                               CoefPrest,
                               Facturation,
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
from core import (Outils, ErreurConsistance, DossierSource, DossierDestination)


class ImportD(object):
    """
    Classe pour l'importation des données nécessaires au module D
    """

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """

        self.dossier_source = dossier_source

        self.edition = Edition(dossier_source)

        if self.edition.filigrane != "":
            chemin = self.edition.chemin_filigrane
        else:
            chemin = self.edition.chemin
        self.chemin_enregistrement = Outils.chemin([chemin, self.edition.plateforme, self.edition.annee,
                                                    Outils.mois_string(self.edition.mois)], self.edition)
        Outils.existe(self.chemin_enregistrement, True)

        chemin_in = Outils.chemin([self.chemin_enregistrement, "IN"], self.edition)
        self.version = 0
        while True:
            self.chemin_version = Outils.chemin([self.chemin_enregistrement, "V"+str(self.version)], self.edition)
            if Outils.existe(self.chemin_version, True):
                self.version = self.version + 1
            else:
                break
        if self.version == 0:
            Outils.existe(chemin_in, True)
            dossier_fixe = dossier_source
            chemin_grille = dossier_source.chemin
        else:
            if not Outils.existe(chemin_in, False):
                Outils.fatal(ErreurConsistance(), "le dossier " + chemin_in + " se doit d'être présent !")
            dossier_fixe = DossierSource(chemin_in)
            chemin_grille = self.chemin_enregistrement

        self.paramtexte = Paramtexte(dossier_fixe)
        self.facturation = Facturation(dossier_fixe)
        self.classes = ClasseClient(dossier_fixe)
        self.clients = Client(dossier_source, self.facturation, self.classes)
        self.plateformes = Plateforme(dossier_fixe, self.clients, self.edition, chemin_grille)
        self.artsap = ArticleSap(dossier_fixe)
        self.categories = Categorie(dossier_fixe, self.artsap, self.plateformes)
        self.groupes = Groupe(dossier_fixe, self.categories)
        self.machines = Machine(dossier_fixe, self.groupes, self.edition)
        self.subsides = Subside(dossier_source)
        self.plafonds = PlafSubside(dossier_source, self.subsides, self.artsap, self.plateformes)
        self.cles = CleSubside(dossier_source, self.clients, self.machines, self.classes, self.subsides)
        self.comptes = Compte(dossier_source, self.clients, self.subsides)
        self.users = User(dossier_source)
        self.categprix = CategPrix(dossier_fixe, self.classes, self.categories)
        self.coefprests = CoefPrest(dossier_fixe, self.classes, self.artsap)
        self.prestations = Prestation(dossier_fixe, self.artsap, self.coefprests, self.plateformes, self.machines,
                                      self.edition)

        self.plateforme = self.plateformes.donnees[self.edition.plateforme]

        self.acces = Acces(dossier_source, self.comptes, self.machines, self.users)
        self.noshows = NoShow(dossier_source, self.comptes, self.machines, self.users)
        self.livraisons = Livraison(dossier_source, self.comptes, self.prestations, self.users)
        self.services = Service(dossier_source, self.comptes, self.categories, self.users)

        if self.edition.mois > 1:
            annee_p = self.edition.annee
            mois_p = Outils.mois_string(self.edition.mois-1)
        else:
            annee_p = self.edition.annee-1
            mois_p = 12
        self.chemin_precedent = Outils.chemin([self.edition.chemin, self.edition.plateforme, annee_p, mois_p, "V0",
                                               "OUT"], self.edition)
        if not Outils.existe(self.chemin_precedent, False):
            Outils.fatal(ErreurConsistance(), "le dossier " + self.chemin_precedent + " se doit d'être présent !")

        self.grants = Granted(DossierSource(self.chemin_precedent), self.edition, self.comptes, self.artsap,
                              self.plateformes)
        self.userlabs = UserLabo(DossierSource(self.chemin_precedent), self.edition, self.plateformes, self.clients,
                                 self.users)

        if self.version == 0:
            dossier_destination = DossierDestination(chemin_in)
            for fichier in [self.paramtexte, self.facturation, self.classes, self.plateformes, self.artsap,
                            self.categories, self.groupes, self.machines, self.categprix, self.coefprests,
                            self.prestations]:
                dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
            for fichier in [self.grants,
                            self.userlabs]:
                dossier_destination.ecrire(fichier.nom_fichier,
                                           DossierSource(self.chemin_precedent).lire(fichier.nom_fichier))
            grille = self.plateforme['grille'] + '.pdf'
            DossierDestination(self.chemin_enregistrement).ecrire(grille, dossier_source.lire(grille))

        chemin_vin = Outils.chemin([self.chemin_version, "IN"], self.edition)
        Outils.existe(chemin_vin, True)
        dossier_destination = DossierDestination(chemin_vin)
        for fichier in [self.clients, self.subsides, self.plafonds, self.cles, self.comptes, self.users,
                        self.acces, self.noshows, self.livraisons, self.services]:
            dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
