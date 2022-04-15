from core import Outils


class UserLaboNew(object):
    """
    Classe pour la création du csv des utilisations des plateformes
    """

    cles = ['year', 'month', 'day', 'week-nbr', 'platf-code', 'platf-op', 'platf-name', 'client-code', 'client-name',
            'client-class', 'user-id', 'user-sciper', 'user-name', 'user-first']

    def __init__(self, imports, transactions, par_user):
        """
        initialisation des données
        :param imports: données importées
        :param transactions: transactions générées
        :param par_user: tri des transactions
        """
        self.valeurs = {}
        self.imports = imports

        self.nom = "User-labo_" + str(imports.edition.annee) + "_" + Outils.mois_string(imports.edition.mois) + ".csv"
        keys = []
        for donnee in imports.userlabs.donnees:
            if imports.edition.annee - donnee['year'] > 1:
                Outils.affiche_message("Comment peut-on avoir des user-labo de plus d'1 année d'écart ?")
                continue
            if imports.edition.annee - donnee['year'] == 1:
                if imports.edition.mois - donnee['month'] > -1:
                    continue
            valeur = []
            for i in range(0, len(self.cles)):
                valeur.append(donnee[self.cles[i]])
            key = str(donnee['year']) + Outils.mois_string(donnee['month']) + donnee['day'] + donnee['user-id'] + \
                donnee['client-code'] + donnee['platf-code']
            if key not in keys:
                keys.append(key)
            else:
                print("doublon", key)
                print(valeur)
                print(self.valeurs[key])
            self.ajouter_valeur(valeur, key)

        for id_user in par_user.keys():
            par_client = par_user[id_user]
            for code in par_client.keys():
                par_jour = par_client[code]['days']
                for jour in par_jour.keys():
                    key = par_jour[jour]
                    trans = transactions.valeurs[key]
                    if (imports.edition.annee == trans['transac-date'].year and
                            imports.edition.mois == trans['transac-date'].month):
                        valeur = [imports.edition.annee, imports.edition.mois]
                        for cle in range(2, len(self.cles)):
                            if self.cles[cle] == 'day':
                                valeur.append(trans['transac-date'].day)
                            elif self.cles[cle] == 'week-nbr':
                                valeur.append(trans['transac-date'].isocalendar()[1])
                            else:
                                valeur.append(trans[self.cles[cle]])
                        self.ajouter_valeur(valeur, str(imports.edition.annee) + str(imports.edition.mois) +
                                            str(trans['transac-date'].day) + id_user + code)

    def ajouter_valeur(self, donnee, unique):
        """
        ajout d'une ligne au prototype de csv
        :param donnee: contenu de la ligne
        :param unique: clé d'identification unique de la ligne
        """
        valeur = {}
        for i in range(0, len(donnee)):
            valeur[self.cles[i]] = donnee[i]
        self.valeurs[unique] = valeur

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
                ligne = []
                for i in range(0, len(self.cles)):
                    ligne.append(valeur[self.cles[i]])
                fichier_writer.writerow(ligne)
