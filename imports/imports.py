from imports import Edition
from imports.constants import (ArticleSap,
                               Categorie,
                               CategPrix,
                               ClasseClient,
                               CoefPrest,
                               Facturation,
                               Groupe,
                               Machine,
                               Paramtexte,
                               Plateforme,
                               Prestation)
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
from imports.construits import (Numero,
                                Granted,
                                UserLabo,
                                Version,
                                Transactions2)
from core import (Interface,
                  Chemin,
                  Format,
                  ErreurConsistance,
                  DossierSource,
                  DossierDestination)


class Imports(object):
    """
    Classe pour l'importation et la strcuturation des données
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
                                                    Format.mois_string(self.edition.mois)], self.edition)
        self.version = 0
        dossier_fixe = dossier_source
        chemin_grille = dossier_source.chemin
        chemin_fixe_version = Chemin.chemin([chemin_fixe_enregistrement, "V0"], self.edition)
        if Chemin.existe(chemin_fixe_enregistrement, False):
            while True:
                if Chemin.existe(chemin_fixe_version, False):
                    self.version = self.version + 1
                    chemin_fixe_version = Chemin.chemin([chemin_fixe_enregistrement, "V"+str(self.version)],
                                                        self.edition)
                else:
                    break

        if self.edition.filigrane != "":
            self.chemin_enregistrement = Chemin.chemin([self.edition.chemin_filigrane, self.edition.plateforme,
                                                        self.edition.annee, Format.mois_string(self.edition.mois)],
                                                       self.edition)
            self.chemin_version = Chemin.chemin([self.chemin_enregistrement, "V" + str(self.version)],
                                                self.edition)
            if Chemin.existe(self.chemin_version, False):
                Interface.fatal(ErreurConsistance(), "la facturation proforma V" + str(self.version) + " existe déjà !")
        else:
            self.chemin_enregistrement = chemin_fixe_enregistrement
            self.chemin_version = chemin_fixe_version

        self.chemin_in = Chemin.chemin([self.chemin_enregistrement, "IN"], self.edition)
        self.chemin_prix = Chemin.chemin([self.chemin_enregistrement, "Prix"], self.edition)
        if self.version > 0:
            self.chemin_in = Chemin.chemin([chemin_fixe_enregistrement, "IN"], self.edition)
            self.chemin_prix = Chemin.chemin([chemin_fixe_enregistrement, "Prix"], self.edition)
            if not Chemin.existe(self.chemin_in, False):
                Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_in + " se doit d'être présent !")
            if not Chemin.existe(self.chemin_prix, False):
                Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_prix + " est censé exister !")
            dossier_fixe = DossierSource(self.chemin_in)
            chemin_grille = chemin_fixe_enregistrement

        self.chemin_out = Chemin.chemin([self.chemin_version, "OUT"], self.edition)
        self.chemin_bilans = Chemin.chemin([self.chemin_version, "Bilans_Stats"], self.edition)
        self.chemin_cannexes = Chemin.chemin([self.chemin_version, "Annexes_CSV"], self.edition)
        self.chemin_pannexes = Chemin.chemin([self.chemin_enregistrement, "Annexes_PDF"], self.edition)

        # importation et vérification des données d'entrée

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

        # importation des données du mois précédent

        if self.edition.mois > 1:
            annee_p = self.edition.annee
            mois_p = Format.mois_string(self.edition.mois-1)
        else:
            annee_p = self.edition.annee-1
            mois_p = 12

        old_ver = 0
        chemin_old = Chemin.chemin([self.edition.chemin, self.edition.plateforme, annee_p, mois_p], self.edition)
        if not Chemin.existe(chemin_old, False):
            Interface.fatal(ErreurConsistance(), "le dossier " + chemin_old + " se doit d'être présent !")
        while True:
            chemin_old_ver = Chemin.chemin([chemin_old, "V"+str(old_ver)], self.edition)
            if Chemin.existe(chemin_old_ver, False):
                old_ver = old_ver + 1
            else:
                old_ver = old_ver - 1
                break

        self.chemin_precedent = Chemin.chemin([chemin_old, "V"+str(old_ver), "OUT"], self.edition)
        if not Chemin.existe(self.chemin_precedent, False):
            Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_precedent + " se doit d'être présent !")

        self.grants = Granted(DossierSource(self.chemin_precedent), self.edition, self.comptes, self.artsap,
                              self.plateformes)
        self.userlabs = UserLabo(DossierSource(self.chemin_precedent), self.edition, self.plateformes, self.clients,
                                 self.users)

        # importation des données de la version précédente
        if self.version > 0:
            vprec = self.version-1
            self.chemin_vprec = Chemin.chemin([chemin_fixe_enregistrement, "V"+str(vprec), "OUT"], self.edition)
            if not Chemin.existe(self.chemin_vprec, False):
                Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_vprec + " se doit d'être présent !")
            self.numeros = Numero(DossierSource(self.chemin_vprec), self.edition, self.comptes, self.clients, vprec)
            self.versions = Version(DossierSource(self.chemin_vprec), self.edition.annee, self.edition.mois, vprec)
            self.chemin_bilprec = Chemin.chemin([chemin_fixe_enregistrement, "V"+str(vprec), "Bilans_Stats"],
                                                self.edition)
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
            for fichier in [self.paramtexte, self.facturation, self.classes, self.plateformes, self.artsap,
                            self.categories, self.groupes, self.machines, self.categprix, self.coefprests,
                            self.prestations]:
                dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
            dossier_precedent = DossierSource(self.chemin_precedent)
            for fichier in [self.grants, self.userlabs]:
                dossier_destination.ecrire(fichier.nom_fichier, dossier_precedent.lire(fichier.nom_fichier))
            if self.plateforme['grille'] != "":
                grille = self.plateforme['grille'] + '.pdf'
                DossierDestination(self.chemin_enregistrement).ecrire(grille, dossier_source.lire(grille))

        if self.version == 0 or self.edition.filigrane != "":
            Chemin.copier_dossier("./reveal.js/", "js", self.chemin_enregistrement)
            Chemin.copier_dossier("./reveal.js/", "css", self.chemin_enregistrement)

        chemin_vin = Chemin.chemin([self.chemin_version, "IN"], self.edition)
        Chemin.existe(chemin_vin, True)
        dossier_destination = DossierDestination(chemin_vin)
        for fichier in [self.clients, self.subsides, self.plafonds, self.cles, self.comptes, self.users,
                        self.acces, self.noshows, self.livraisons, self.services]:
            dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
        if self.version > 0:
            for fichier in [self.numeros, self.versions]:
                dossier_destination.ecrire(fichier.nom_fichier,
                                           DossierSource(self.chemin_vprec).lire(fichier.nom_fichier))
            dossier_destination.ecrire(self.transactions_2.nom_fichier,
                                       DossierSource(self.chemin_bilprec).lire(self.transactions_2.nom_fichier))
