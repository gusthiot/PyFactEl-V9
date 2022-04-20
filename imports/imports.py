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
                                UserLabo)
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

        if self.edition.filigrane != "":
            chemin = self.edition.chemin_filigrane
        else:
            chemin = self.edition.chemin
        self.chemin_enregistrement = Chemin.chemin([chemin, self.edition.plateforme, self.edition.annee,
                                                    Format.mois_string(self.edition.mois)], self.edition)

        self.version = 0
        dossier_fixe = dossier_source
        chemin_grille = dossier_source.chemin
        self.chemin_in = Chemin.chemin([self.chemin_enregistrement, "IN"], self.edition)
        self.chemin_version = Chemin.chemin([self.chemin_enregistrement, "V0"], self.edition)
        if Chemin.existe(self.chemin_enregistrement, False):
            while True:
                if Chemin.existe(self.chemin_version, False):
                    self.version = self.version + 1
                    self.chemin_version = Chemin.chemin([self.chemin_enregistrement, "V"+str(self.version)],
                                                        self.edition)
                else:
                    break

            if self.version > 0:
                if not Chemin.existe(self.chemin_in, False):
                    Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_in + " se doit d'être présent !")
                dossier_fixe = DossierSource(self.chemin_in)
                chemin_grille = self.chemin_enregistrement

        self.chemin_out = Chemin.chemin([self.chemin_version, "OUT"], self.edition)
        self.chemin_bilans = Chemin.chemin([self.chemin_version, "Bilans_Stats"], self.edition)
        self.chemin_prix = Chemin.chemin([self.chemin_enregistrement, "Prix"], self.edition)
        self.chemin_cannexes = Chemin.chemin([self.chemin_version, "Annexes_CSV"], self.edition)

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

        if self.edition.mois > 1:
            annee_p = self.edition.annee
            mois_p = Format.mois_string(self.edition.mois-1)
        else:
            annee_p = self.edition.annee-1
            mois_p = 12

        old_ver = 0
        while True:
            self.chemin_old_ver = Chemin.chemin([self.edition.chemin, self.edition.plateforme, annee_p, mois_p,
                                                 "V"+str(old_ver)], self.edition)
            if Chemin.existe(self.chemin_old_ver, False):
                old_ver = old_ver + 1
            else:
                old_ver = old_ver - 1
                break

        self.chemin_precedent = Chemin.chemin([self.edition.chemin, self.edition.plateforme, annee_p, mois_p,
                                               "V"+str(old_ver), "OUT"], self.edition)
        if not Chemin.existe(self.chemin_precedent, False):
            Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_precedent + " se doit d'être présent !")

        self.grants = Granted(DossierSource(self.chemin_precedent), self.edition, self.comptes, self.artsap,
                              self.plateformes)
        self.userlabs = UserLabo(DossierSource(self.chemin_precedent), self.edition, self.plateformes, self.clients,
                                 self.users)
        if self.version > 0:
            self.chemin_vprec = Chemin.chemin([self.chemin_enregistrement, "V"+str(self.version-1), "OUT"],
                                              self.edition)
            if not Chemin.existe(self.chemin_vprec, False):
                Interface.fatal(ErreurConsistance(), "le dossier " + self.chemin_vprec + " se doit d'être présent !")
            self.numeros = Numero(DossierSource(self.chemin_vprec), self.edition, self.comptes, self.clients,
                                  self.version-1)

        # vérification terminée, création des dossiers de sauvegarde

        if self.version == 0:
            Chemin.existe(self.chemin_in, True)
        Chemin.existe(self.chemin_prix, True)
        Chemin.existe(self.chemin_bilans, True)
        Chemin.existe(self.chemin_out, True)
        Chemin.existe(self.chemin_cannexes, True)

        # sauvegarde des bruts

        if self.version == 0:
            dossier_destination = DossierDestination(self.chemin_in)
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

        chemin_vin = Chemin.chemin([self.chemin_version, "IN"], self.edition)
        Chemin.existe(chemin_vin, True)
        dossier_destination = DossierDestination(chemin_vin)
        for fichier in [self.clients, self.subsides, self.plafonds, self.cles, self.comptes, self.users,
                        self.acces, self.noshows, self.livraisons, self.services]:
            dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
        if self.version > 0:
            dossier_vprec = DossierSource(self.chemin_vprec)
            dossier_destination.ecrire(self.numeros.nom_fichier, dossier_vprec.lire(self.numeros.nom_fichier))

        # dossier_lien = Outils.lien_dossier([import_d.facturation.lien, plateforme, annee, Outils.mois_string(mois)],
        #                                    import_d.facturation)
        #
        # dossier_pannexes = Chemin.chemin([dossier_enregistrement, "Annexes_PDF"], import_d.facturation)
        # Chemin.existe(dossier_pannexes, True)
        #