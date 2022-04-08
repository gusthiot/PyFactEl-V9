import sys
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


class ImportD(object):

    def __init__(self, dossier_source):

        self.generaux = Generaux(dossier_source)

        self.edition = Edition(dossier_source)
        self.paramtexte = Paramtexte(dossier_source)

        self.acces = Acces(dossier_source)
        self.categories = Categorie(dossier_source)
        self.categprix = CategPrix(dossier_source)
        self.clients = Client(dossier_source)
        self.coefprests = CoefPrest(dossier_source)
        self.comptes = Compte(dossier_source)
        self.grants = Granted(dossier_source, self.edition)
        self.userlabs = UserLabo(dossier_source, self.edition)
        self.livraisons = Livraison(dossier_source)
        self.machines = Machine(dossier_source)
        self.groupes = Groupe(dossier_source)
        self.noshows = NoShow(dossier_source)
        self.plafonds = PlafSubside(dossier_source)
        self.plateformes = Plateforme(dossier_source)
        self.prestations = Prestation(dossier_source)
        self.subsides = Subside(dossier_source)
        self.cles = CleSubside(dossier_source)
        self.users = User(dossier_source)
        self.classes = ClasseClient(dossier_source)
        self.artsap = ArticleSap(dossier_source)
        self.services = Service(dossier_source)
        self.dossier_source = dossier_source

        if self.verification_coherence() > 0:
            sys.exit("Erreur dans la cohérence")

    def copie_fixes(self, dossier_destination):
        for fichier in [self.paramtexte, self.generaux, self.classes, self.plateformes, self.artsap, self.categories,
                        self.groupes, self.machines, self.categprix, self.coefprests, self.prestations, self.grants,
                        self.userlabs]:
            dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))

    def copie_variables(self, dossier_destination):
        for fichier in [self.clients, self.subsides, self.plafonds, self.cles, self.comptes, self.users,
                        self.acces, self.noshows, self.livraisons, self.services]:
            dossier_destination.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))

    def verification_coherence(self):
        """
        vérifie la cohérence des données importées
        :return: 0 si ok, sinon le nombre d'échecs à la vérification
        """
        verif = 0
        verif += self.artsap.est_coherent()
        verif += self.classes.est_coherent()
        verif += self.clients.est_coherent(self.generaux, self.classes)
        verif += self.plateformes.est_coherent(self.clients, self.dossier_source)
        verif += self.edition.est_coherent(self.plateformes)
        verif += self.users.est_coherent()
        verif += self.categories.est_coherent(self.artsap, self.plateformes)
        verif += self.groupes.est_coherent(self.categories)
        verif += self.machines.est_coherent(self.groupes)
        verif += self.categprix.est_coherent(self.classes, self.categories)
        verif += self.coefprests.est_coherent(self.classes, self.artsap)
        verif += self.prestations.est_coherent(self.artsap, self.coefprests, self.plateformes, self.machines)
        verif += self.subsides.est_coherent()
        verif += self.plafonds.est_coherent(self.subsides, self.artsap, self.plateformes)
        verif += self.cles.est_coherent(self.clients, self.machines, self.classes, self.subsides)
        verif += self.comptes.est_coherent(self.clients, self.subsides)
        verif += self.grants.est_coherent(self.comptes, self.artsap, self.plateformes)
        verif += self.userlabs.est_coherent(self.plateformes, self.clients, self.users)
        verif += self.acces.est_coherent(self.comptes, self.machines, self.users)
        verif += self.noshows.est_coherent(self.comptes, self.machines, self.users)
        verif += self.livraisons.est_coherent(self.comptes, self.prestations, self.users)
        verif += self.services.est_coherent(self.comptes, self.categories, self.users)

        return verif
