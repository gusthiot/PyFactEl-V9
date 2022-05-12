from core import (Interface,
                  Format,
                  CsvDict)
from imports.construits import UserLabo


class UserLaboNew(CsvDict):
    """
    Classe pour la création du csv des utilisations des plateformes
    """

    def __init__(self, imports, transactions_3, par_user):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_user: tri des transactions
        """
        super().__init__(imports)

        self.cles = UserLabo.cles
        self.nom = "User-labo_" + str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) + ".csv"
        keys = []
        for donnee in imports.userlabs.donnees:
            if imports.edition.annee - donnee['year'] > 1:
                Interface.affiche_message("Comment peut-on avoir des user-labo de plus d'1 année d'écart ?")
                continue
            if imports.edition.annee - donnee['year'] == 1:
                if imports.edition.mois - donnee['month'] > -1:
                    continue
            valeur = []
            for i in range(0, len(UserLabo.cles)):
                valeur.append(donnee[UserLabo.cles[i]])
            key = str(donnee['year']) + Format.mois_string(donnee['month']) + donnee['day'] + donnee['user-id'] + \
                donnee['client-code'] + donnee['platf-code']
            if key not in keys:
                keys.append(key)
            else:
                print("doublon", key)
                print(valeur)
                print(self.valeurs[key])
            self._ajouter_valeur(valeur, key)

        for id_user, par_client in par_user.items():
            for code, par_code in par_client.items():
                for jour in par_code['days'].values():
                    trans = transactions_3.valeurs[jour]
                    valeur = [imports.edition.annee, imports.edition.mois]
                    for cle in range(2, len(UserLabo.cles)):
                        if UserLabo.cles[cle] == 'day':
                            valeur.append(trans['transac-date'].day)
                        elif UserLabo.cles[cle] == 'week-nbr':
                            valeur.append(trans['transac-date'].isocalendar()[1])
                        else:
                            valeur.append(trans[UserLabo.cles[cle]])
                    self._ajouter_valeur(valeur, str(imports.edition.annee) + str(imports.edition.mois) +
                                         str(trans['transac-date'].day) + id_user + code)
