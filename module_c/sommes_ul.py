

class SommesUL(object):
    """
    Classe pour sommer les users labos
    """

    def __init__(self, usr_lab, imports):
        """
        initialisation des données
        :param usr_lab: données users labos
        :param imports: données importées
        """

        self.par_ul = {'annees': {}, 'semaines': {}}
        for valeur in usr_lab.valeurs.values():
            annee = valeur['year']
            mois = valeur['month']
            pan = self.par_ul['annees']
            if annee not in pan:
                pan[annee] = {}
            if mois not in pan[annee]:
                pan[annee][mois] = {'users': [], 'jours': {}, 'clients': {}}
            pm = pan[annee][mois]
            code = valeur['client-code']
            id_plateforme = valeur['platf-code']
            user = valeur['user-id']
            if id_plateforme != code:
                if mois == imports.edition.mois:
                    jour = valeur['day']
                    if jour not in pm['jours']:
                        pm['jours'][jour] = []
                    if user not in pm['jours'][jour]:
                        pm['jours'][jour].append(user)
                if user not in pm['users']:
                    pm['users'].append(user)
                semaine = valeur['week-nbr']
                pse = self.par_ul['semaines']
                if semaine not in pse:
                    pse[semaine] = []
                if user not in pse[semaine]:
                    pse[semaine].append(user)

            if code not in pm['clients']:
                pm['clients'][code] = []
            if user not in pm['clients'][code]:
                pm['clients'][code].append(user)
