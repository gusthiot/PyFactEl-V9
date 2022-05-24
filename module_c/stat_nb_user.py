from core import (Format,
                  CsvList)
from calendar import monthrange
from datetime import datetime


class StatNbUser(CsvList):
    """
    Classe pour la création du csv des stats nombre user
    """

    cles = ['year', 'month', 'day', 'week-nbr', 'stat-nbuser-d', 'stat-nbuser-w', 'stat-nbuser-m', 'stat-nbuser-3m',
            'stat-nbuser-6m', 'stat-nbuser-12m']

    def __init__(self, imports, par_ul):
        """
        initialisation des données
        :param imports: données importées
        :param par_ul: tri des users labo
        """
        super().__init__(imports)

        self.nom = "Stat-nbre-user_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" \
                   + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        jour_de_semaine, nb_de_jours = monthrange(imports.edition.annee, imports.edition.mois)
        for jour in range(1, nb_de_jours+1):
            nb_user_d = 0
            nb_user_m = ""
            nb_user_3m = ""
            nb_user_6m = ""
            nb_user_12m = ""
            pmu = []
            if imports.edition.annee in par_ul['annees'] and \
                    imports.edition.mois in par_ul['annees'][imports.edition.annee]:
                pm = par_ul['annees'][imports.edition.annee][imports.edition.mois]
                pmu = pm['users']
                if jour in pm['jours']:
                    nb_user_d = len(pm['jours'][jour])
            if jour == nb_de_jours:
                nb_user_m = len(pmu)
                user_3m = pmu.copy()
                user_6m = pmu.copy()
                user_12m = pmu.copy()
                for gap in range(1, 12):
                    if gap < imports.edition.mois:
                        mo = imports.edition.mois - gap
                        an = imports.edition.annee
                    else:
                        mo = 12 + imports.edition.mois - gap
                        an = imports.edition.annee - 1
                    if an in par_ul['annees']:
                        if mo in par_ul['annees'][an]:
                            ids = par_ul['annees'][an][mo]['users']
                            for idd in ids:
                                if gap < 3 and idd not in user_3m:
                                    user_3m.append(idd)
                                if gap < 6 and idd not in user_6m:
                                    user_6m.append(idd)
                                if idd not in user_12m:
                                    user_12m.append(idd)

                nb_user_3m = len(user_3m)
                nb_user_6m = len(user_6m)
                nb_user_12m = len(user_12m)
            date = datetime(imports.edition.annee, imports.edition.mois, jour)
            semaine = date.isocalendar()[1]
            nb_user_w = ""
            if date.weekday() == 6:
                if semaine in par_ul['semaines']:
                    nb_user_w = len(par_ul['semaines'][semaine])
                else:
                    nb_user_w = 0
            ligne = [imports.edition.annee, imports.edition.mois, jour, semaine, nb_user_d, nb_user_w, nb_user_m,
                     nb_user_3m, nb_user_6m, nb_user_12m]
            self.lignes.append(ligne)
