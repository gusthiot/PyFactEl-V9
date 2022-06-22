from imports import Edition
from imports.constants import (ArticleSap,
                               ClasseClient,
                               Facturation,
                               Paramtexte,
                               Plateforme)
from imports.variables import (Client,
                               Data)
from imports.construits import (Version,
                                Transactions2)
from core import (Interface,
                  Chemin,
                  Format,
                  ErreurConsistance,
                  DossierSource,
                  DossierDestination)


class ImportsA(object):
    """
    Classe pour l'importation et la structuration des données pour uniquement le module A
    """

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """

        self.dossier_source = dossier_source

        self.edition = Edition(dossier_source)

        # création de l'arobrescence

        chemin_fixe_enregistrement = Chemin.chemin([self.edition.chemin, self.edition.plateforme, self.edition.annee,
                                                    Format.mois_string(self.edition.mois)])
        self.version = 0
        dossier_fixe = dossier_source
        self.chemin_logo = dossier_source.chemin
        chemin_grille = dossier_source.chemin
        chemin_fixe_version = Chemin.chemin([chemin_fixe_enregistrement, "V0"])
        if Chemin.existe(chemin_fixe_enregistrement, False):
            while True:
                if Chemin.existe(chemin_fixe_version, False):
                    self.version = self.version + 1
                    chemin_fixe_version = Chemin.chemin([chemin_fixe_enregistrement, "V"+str(self.version)])
                else:
                    break

        if self.edition.filigrane != "":
            self.chemin_enregistrement = Chemin.chemin([self.edition.chemin_filigrane, self.edition.plateforme,
                                                        self.edition.annee, Format.mois_string(self.edition.mois)])
            self.chemin_version = Chemin.chemin([self.chemin_enregistrement, "V" + str(self.version)])
            if Chemin.existe(self.chemin_version, False):
                Interface.fatal(ErreurConsistance(), "la facturation proforma V" + str(self.version) + " existe déjà !")
        else:
            self.chemin_enregistrement = chemin_fixe_enregistrement
            self.chemin_version = chemin_fixe_version

        self.chemin_in = Chemin.chemin([self.chemin_enregistrement, "IN"])
        self.chemin_prix = Chemin.chemin([self.chemin_enregistrement, "Prix"])
        if self.version > 0:
            self.chemin_in = Chemin.chemin([chemin_fixe_enregistrement, "IN"])
            self.chemin_prix = Chemin.chemin([chemin_fixe_enregistrement, "Prix"])
            if not Chemin.existe(self.chemin_in, False):
                Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_in + " se doit d'être présent !")
            if not Chemin.existe(self.chemin_prix, False):
                Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_prix + " est censé exister !")
            dossier_fixe = DossierSource(self.chemin_in)
            self.chemin_logo = self.chemin_in
            chemin_grille = chemin_fixe_enregistrement

        self.chemin_out = Chemin.chemin([self.chemin_version, "OUT"])
        self.chemin_bilans = Chemin.chemin([self.chemin_version, "Bilans_Stats"])
        self.chemin_cannexes = Chemin.chemin([self.chemin_version, "Annexes_CSV"])
        self.chemin_pannexes = Chemin.chemin([self.chemin_enregistrement, "Annexes_PDF"])

        # importation et vérification des données d'entrée

        self.paramtexte = Paramtexte(dossier_fixe)
        self.facturation = Facturation(dossier_fixe)
        self.classes = ClasseClient(dossier_fixe, True)
        self.clients = Client(dossier_source, self.facturation, self.classes)
        self.plateformes = Plateforme(dossier_fixe, self.clients, self.edition, chemin_grille)
        self.artsap = ArticleSap(dossier_fixe, True)
        self.data = Data(dossier_source, self.clients, self.artsap)

        self.plateforme = self.plateformes.donnees[self.edition.plateforme]

        self.logo = ""
        extensions = [".pdf", ".eps", ".png", ".jpg"]
        for ext in extensions:
            chemin = Chemin.chemin([self.chemin_logo, "logo" + ext])
            if Chemin.existe(chemin, False):
                self.logo = "logo" + ext
                break

        # importation des données de la version précédente
        if self.version > 0:
            vprec = self.version-1
            self.chemin_vprec = Chemin.chemin([chemin_fixe_enregistrement, "V"+str(vprec), "OUT"])
            if not Chemin.existe(self.chemin_vprec, False):
                Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_vprec + " se doit d'être présent !")
            self.versions = Version(DossierSource(self.chemin_vprec), self.edition.annee, self.edition.mois, vprec)
            self.chemin_bilprec = Chemin.chemin([chemin_fixe_enregistrement, "V"+str(vprec), "Bilans_Stats"])
            if not Chemin.existe(self.chemin_bilprec, False):
                Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_bilprec + " se doit d'être présent !")
            self.transactions_2 = Transactions2(DossierSource(self.chemin_bilprec), self.edition.annee,
                                                self.edition.mois, self.plateforme, vprec)

        # vérification terminée, création des dossiers de sauvegarde

        if self.version == 0:
            Chemin.existe(self.chemin_in, True)
            Chemin.existe(self.chemin_prix, True)
        Chemin.existe(self.chemin_bilans, True)
        Chemin.existe(self.chemin_out, True)
        Chemin.existe(self.chemin_cannexes, True)
        Chemin.existe(self.chemin_pannexes, True)

        # sauvegarde des bruts

        if self.version == 0:
            dossier_destination = DossierDestination(self.chemin_in)
            for fichier in [self.paramtexte, self.facturation, self.classes, self.plateformes, self.artsap]:
                dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
            if self.logo != "":
                dossier_destination.ecrire(self.logo, dossier_source.lire(self.logo))
            if self.plateforme['grille'] != "":
                grille = self.plateforme['grille'] + '.pdf'
                DossierDestination(self.chemin_enregistrement).ecrire(grille, dossier_source.lire(grille))

        if self.version == 0 or self.edition.filigrane != "":
            Chemin.copier_dossier("./reveal.js/", "js", self.chemin_enregistrement)
            Chemin.copier_dossier("./reveal.js/", "css", self.chemin_enregistrement)

        chemin_vin = Chemin.chemin([self.chemin_version, "IN"])
        Chemin.existe(chemin_vin, True)
        dossier_destination = DossierDestination(chemin_vin)
        for fichier in [self.clients, self.data]:
            dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
        if self.version > 0:
            dossier_destination.ecrire(self.versions.nom_fichier,
                                       DossierSource(self.chemin_vprec).lire(self.versions.nom_fichier))
            dossier_destination.ecrire(self.transactions_2.nom_fichier,
                                       DossierSource(self.chemin_bilprec).lire(self.transactions_2.nom_fichier))
