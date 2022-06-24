from core import (Format, CsvDict)


class Transactions3(CsvDict):
    """
    Classe pour la création des transactions de niveau 3
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-project', 'client-code', 'client-sap',
            'client-name', 'client-idclass', 'client-class', 'client-labelclass', 'oper-id', 'oper-name', 'oper-note',
            'staff-note', 'mach-id', 'mach-name', 'mach-extra', 'user-id', 'user-sciper', 'user-name', 'user-first',
            'proj-id', 'proj-nbr', 'proj-name', 'proj-expl', 'flow-type', 'item-id', 'item-codeK', 'item-textK',
            'item-text2K', 'item-nbr', 'item-name', 'item-unit', 'item-idsap', 'item-codeD', 'item-flag-usage',
            'item-flag-conso', 'item-eligible', 'item-order', 'item-labelcode', 'item-extra', 'platf-code', 'platf-op',
            'platf-name', 'transac-date', 'transac-quantity', 'transac-valid', 'transac-id-staff', 'transac-staff',
            'transac-usage', 'transac-runtime', 'transac-runcae', 'valuation-price', 'valuation-brut', 'discount-type',
            'discount-CHF', 'valuation-net', 'subsid-code', 'subsid-name', 'subsid-start', 'subsid-end', 'subsid-ok',
            'subsid-pourcent', 'subsid-maxproj', 'subsid-maxmois', 'subsid-reste', 'subsid-CHF', 'deduct-CHF',
            'subsid-deduct', 'total-fact', 'discount-bonus', 'subsid-bonus']

    def __init__(self, imports, articles, tarifs):
        """
        initialisation des données
        :param imports: données importées
        :param articles: articles générés
        :param tarifs: tarifs générés
        """
        super().__init__(imports)
        self.nom = "Transaction3_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" \
                   + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"
        self.comptabilises = {}
        self.valeurs = {}

        pt = imports.paramtexte.donnees
        transacts = {}

        for entree in imports.acces.donnees:
            if entree['validation'] == '0':
                continue
            compte = imports.comptes.donnees[entree['id_compte']]
            client = imports.clients.donnees[compte['code_client']]
            id_classe = client['id_classe']
            classe = imports.classes.donnees[id_classe]
            id_machine = entree['id_machine']
            machine = imports.machines.donnees[id_machine]
            groupe = imports.groupes.donnees[machine['id_groupe']]
            operateur = imports.users.donnees[entree['id_op']]
            ope = [entree['id_op'], operateur['prenom'] + " " + operateur['nom'], entree['remarque_op'],
                   entree['remarque_staff'], id_machine, machine['nom'], ""]
            util_proj = self.__util_proj(entree['id_user'], compte, pt['flow-cae'])
            counted = False
            duree_hp = round(entree['duree_machine_hp']/60, 3)
            duree_hc = round(entree['duree_machine_hc']/60, 3)
            duree_op = round(entree['duree_operateur']/60, 3)

            if duree_hp > 0 or duree_hc > 0:
                # K3 CAE-run #
                id_groupe = groupe['id_cat_plat']
                if id_groupe != '0' and duree_op == 0:
                    article = articles.valeurs[id_groupe]
                    if imports.edition.plateforme == article['platf-code']:
                        ref_client = self.__ref_client(entree['annee'], entree['mois'], classe, client, compte, article)
                        tarif = tarifs.valeurs[id_classe + id_groupe]
                        art = self.__art_plate(article, "K3", pt['item-K3'], pt['item-K3a'])
                        if article['platf-code'] == compte['code_client']:
                            usage = 0
                            if compte['exploitation'] == "TRUE":
                                runcae = ""
                            else:
                                runcae = 1
                                counted = True
                        elif entree['validation'] == "2":
                            usage = 0
                            runcae = ""
                        else:
                            usage = 1
                            runcae = 1
                            counted = True
                        trans = [entree['date_login'], 1] + self.__staff(entree) + [usage, "", runcae]
                        val = [tarif['valuation-price'], tarif['valuation-price'], "", 0, tarif['valuation-price']]
                        self.__put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val)

                # K7 CAE-runf #
                id_groupe = groupe['id_cat_fixe']
                if id_groupe != '0':
                    article = articles.valeurs[id_groupe]
                    if imports.edition.plateforme == article['platf-code']:
                        ref_client = self.__ref_client(entree['annee'], entree['mois'], classe, client, compte, article)
                        tarif = tarifs.valeurs[id_classe + id_groupe]
                        art = self.__art_plate(article, "K7", pt['item-K7'], pt['item-K7a'])
                        if ((article['platf-code'] == compte['code_client'] and compte['exploitation'] == "TRUE")
                                or entree['validation'] == "2"):
                            usage = 0
                            runcae = ""
                        else:
                            usage = 1
                            if counted:
                                runcae = ""
                            else:
                                runcae = 1
                                counted = True
                        trans = [entree['date_login'], 1] + self.__staff(entree) + [usage, "", runcae]
                        val = [tarif['valuation-price'], tarif['valuation-price'], "", 0, tarif['valuation-price']]
                        self.__put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val)

                # K4 CAE-Extra #
                id_groupe = groupe['id_cat_cher']
                if id_groupe != '0':
                    prix_extra = imports.categprix.donnees[id_classe + id_groupe]['prix_unit']
                    if prix_extra > 0:
                        article = articles.valeurs[id_groupe]
                        if imports.edition.plateforme == article['platf-code']:
                            ref_client = self.__ref_client(entree['annee'], entree['mois'], classe, client, compte,
                                                           article)
                            tarif = tarifs.valeurs[id_classe + id_groupe]
                            duree = duree_hp + duree_hc
                            if ((article['platf-code'] == compte['code_client'] and compte['exploitation'] == "TRUE")
                                    or entree['validation'] == "2"):
                                usage = 0
                                runcae = ""
                            else:
                                usage = duree
                                if counted:
                                    runcae = ""
                                else:
                                    runcae = 1
                                    counted = True
                            trans = [entree['date_login'], duree] + self.__staff(entree) + [usage, "", runcae]
                            art = self.__art_plate(article, "K4", pt['item-K4'], pt['item-K4a'])
                            prix = round(duree * tarif['valuation-price'], 2)
                            val = [tarif['valuation-price'], prix, "", 0, prix]
                            self.__put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val)

            # K1 ...
            id_groupe = groupe['id_cat_mach']
            if id_groupe != '0':
                article = articles.valeurs[id_groupe]
                if imports.edition.plateforme == article['platf-code']:
                    ref_client = self.__ref_client(entree['annee'], entree['mois'], classe, client, compte, article)
                    tarif = tarifs.valeurs[id_classe + id_groupe]

                    # K1 CAE-HP #
                    if duree_hp > 0:
                        if ((article['platf-code'] == compte['code_client'] and compte['exploitation'] == "TRUE")
                                or entree['validation'] == "2"):
                            usage = 0
                            runtime = ""
                            runcae = ""
                        else:
                            usage = duree_hp
                            runtime = round(entree['duree_run']/60, 3)
                            if counted:
                                runcae = ""
                            else:
                                runcae = 1
                                counted = True
                        art = self.__art_plate(article, "K1", pt['item-K1'], pt['item-K1a'])
                        trans = [entree['date_login'], duree_hp] + self.__staff(entree) + [usage, runtime, runcae]
                        prix = round(duree_hp * tarif['valuation-price'], 2)
                        val = [tarif['valuation-price'], prix, "", 0, prix]
                        self.__put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val)

                    # K1 CAE-HC #
                    if duree_hc > 0:
                        if ((article['platf-code'] == compte['code_client'] and compte['exploitation'] == "TRUE")
                                or entree['validation'] == "2"):
                            usage = 0
                            runtime = ""
                            runcae = ""
                        else:
                            usage = duree_hc
                            if duree_hp > 0:
                                runtime = ""
                            else:
                                runtime = round(entree['duree_run']/60, 3)
                            if counted:
                                runcae = ""
                            else:
                                runcae = 1
                                counted = True
                        art = self.__art_plate(article, "K1", pt['item-K1'], pt['item-K1b'])
                        trans = [entree['date_login'], duree_hc] + self.__staff(entree) + [usage, runtime, runcae]
                        prix = round(duree_hc * tarif['valuation-price'], 2)
                        reduc = round(tarif['valuation-price'] * machine['tx_rabais_hc']/100 * duree_hc, 2)
                        val = [tarif['valuation-price'], prix,
                               pt['discount-HC'] + " -" + str(machine['tx_rabais_hc']) + "%", reduc, prix-reduc]
                        self.__put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val)

            # K2 CAE-MO #
            id_groupe = groupe['id_cat_mo']
            if id_groupe != '0' and duree_op > 0:
                article = articles.valeurs[id_groupe]
                if imports.edition.plateforme == article['platf-code']:
                    ref_client = self.__ref_client(entree['annee'], entree['mois'], classe, client, compte, article)
                    tarif = tarifs.valeurs[id_classe + id_groupe]
                    art = self.__art_plate(article, "K2", pt['item-K2'], pt['item-K2a'])
                    if article['platf-code'] == compte['code_client']:
                        usage = 0
                        if compte['exploitation'] == "TRUE":
                            runcae = ""
                        else:
                            if counted:
                                runcae = ""
                            else:
                                runcae = 1
                    elif entree['validation'] == "2":
                        usage = 0
                        runcae = ""
                    else:
                        usage = duree_op
                        if counted:
                            runcae = ""
                        else:
                            runcae = 1
                    trans = [entree['date_login'], duree_op] + self.__staff(entree) + [usage, "", runcae]
                    prix = round(duree_op * tarif['valuation-price'], 2)
                    val = [tarif['valuation-price'], prix, "", 0, prix]
                    self.__put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val)

        for entree in imports.noshows.donnees:
            if entree['validation'] == '0':
                continue
            compte = imports.comptes.donnees[entree['id_compte']]
            client = imports.clients.donnees[compte['code_client']]
            id_classe = client['id_classe']
            classe = imports.classes.donnees[id_classe]
            id_machine = entree['id_machine']
            machine = imports.machines.donnees[id_machine]
            groupe = imports.groupes.donnees[machine['id_groupe']]
            if entree['type'] == 'HP':
                # K5 NoShow-HP #
                id_groupe = groupe['id_cat_hp']
                code = "K5"
                texte = pt['item-K5']
                texte2 = pt['item-K5a']
            else:
                # K6 NoShow-HC #
                id_groupe = groupe['id_cat_hc']
                code = "K6"
                texte = pt['item-K6']
                texte2 = pt['item-K6a']

            if id_groupe != '0':
                article = articles.valeurs[id_groupe]
                if imports.edition.plateforme == article['platf-code']:
                    ref_client = self.__ref_client(entree['annee'], entree['mois'], classe, client, compte, article)
                    tarif = tarifs.valeurs[id_classe + id_groupe]
                    ope = ["", "", "", "", id_machine, machine['nom'], ""]
                    util_proj = self.__util_proj(entree['id_user'], compte, pt['flow-noshow'])
                    art = self.__art_plate(article, code, texte, texte2)
                    trans = [entree['date_debut'], entree['penalite']] + self.__staff(entree) + [0, "", ""]
                    prix = round(entree['penalite'] * tarif['valuation-price'], 2)
                    val = [tarif['valuation-price'], prix, "", 0, prix]
                    self.__put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val)

        for entree in imports.livraisons.donnees:
            if entree['validation'] == '0':
                continue
            compte = imports.comptes.donnees[entree['id_compte']]
            client = imports.clients.donnees[compte['code_client']]
            id_classe = client['id_classe']
            classe = imports.classes.donnees[id_classe]
            id_prestation = entree['id_prestation']
            prestation = imports.prestations.donnees[id_prestation]
            operateur = imports.users.donnees[entree['id_operateur']]
            id_machine = prestation['id_machine']
            article = articles.valeurs[id_prestation]
            if imports.edition.plateforme == article['platf-code']:
                ref_client = self.__ref_client(entree['annee'], entree['mois'], classe, client, compte, article)
                tarif = tarifs.valeurs[id_classe + id_prestation]
                if id_machine == "0":
                    # LVR-mag #
                    idm = ""
                    nm = ""
                    extra = ""
                else:
                    # LVR-mach #
                    idm = id_machine
                    machine = imports.machines.donnees[id_machine]
                    groupe = imports.groupes.donnees[machine['id_groupe']]
                    nm = machine['nom']
                    extra = groupe['id_cat_mach']
                art = self.__art_plate(article, "", "", "")
                ope = [entree['id_operateur'], operateur['prenom'] + " " + operateur['nom'],
                       pt['oper-PO'] + " " + str(entree['date_commande']), entree['remarque'], idm, nm, extra]
                util_proj = self.__util_proj(entree['id_user'], compte, pt['flow-lvr'])
                trans = [entree['date_livraison'], entree['quantite']] + self.__staff(entree) + [0, "", ""]
                if entree['rabais'] > 0:
                    discount = pt['discount-LVR']
                else:
                    discount = ""
                prix = round(entree['quantite'] * tarif['valuation-price'], 2)
                val = [tarif['valuation-price'], prix, discount, entree['rabais'], prix-entree['rabais']]
                self.__put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val)

        # SRV
        for entree in imports.services.donnees:
            if entree['validation'] == '0':
                continue
            compte = imports.comptes.donnees[entree['id_compte']]
            client = imports.clients.donnees[compte['code_client']]
            id_classe = client['id_classe']
            id_categorie = entree['id_categorie']
            classe = imports.classes.donnees[id_classe]
            operateur = imports.users.donnees[entree['id_op']]
            article = articles.valeurs[id_categorie]
            if imports.edition.plateforme == article['platf-code']:
                ref_client = self.__ref_client(entree['annee'], entree['mois'], classe, client, compte, article)
                tarif = tarifs.valeurs[id_classe + id_categorie]
                ope = [entree['id_op'], operateur['prenom'] + " " + operateur['nom'], "", entree['remarque_staff'],
                       "", "", ""]
                util_proj = self.__util_proj(entree['id_user'], compte, pt['flow-srv'])
                art = self.__art_plate(article, "", "", "")
                if ((article['platf-code'] == compte['code_client'] and compte['exploitation'] == "TRUE")
                        or entree['validation'] == "2"):
                    usage = 0
                else:
                    usage = entree['quantite']
                trans = [entree['date'], entree['quantite']] + self.__staff(entree) + [usage, "", ""]
                prix = round(entree['quantite'] * tarif['valuation-price'], 2)
                val = [tarif['valuation-price'], prix, "", 0, prix]
                self.__put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val)

        # subsides et montants
        i = 0
        for trf in sorted(transacts.keys()):
            for trt in sorted(transacts[trf].keys()):
                tarray = transacts[trf][trt]
                for transact in tarray:
                    article = articles.valeurs[transact['art'][0]]
                    subs = self.__subsides(transact, article)
                    if self.imports.classes.donnees[transact['rc'][7]]['subsides'] == "BONUS":
                        if transact['trans'][2] == "1":
                            ded_bon = transact['val'][3]
                        else:
                            ded_bon = 0
                        ded_rab = 0
                        sub_bon = subs[9]
                        sub_rab = 0
                    else:
                        ded_bon = 0
                        if transact['trans'][2] == "1":
                            ded_rab = transact['val'][3]
                        else:
                            ded_rab = 0
                        sub_bon = 0
                        sub_rab = subs[9]
                    id_compte = transact['up'][4]
                    compte = imports.comptes.donnees[id_compte]
                    if article['platf-code'] == compte['code_client'] or transact['trans'][2] != "1":
                        tot = 0
                    else:
                        tot = transact['val'][1] - ded_rab - sub_rab
                    mont = [ded_rab, sub_rab, tot, ded_bon, sub_bon]
                    donnee = transact['rc'] + transact['ope'] + transact['up'] + transact['art'] + transact['trans'] + \
                        transact['val'] + subs + mont
                    self._ajouter_valeur(donnee, i)
                    i = i + 1

    def __staff(self, entree):
        """
        détermine les paramètres lié au staff de validation
        :param entree: ligne d'entrée
        :return: id du staff (vide si "0"), et nom du staff (vide si "0")
        """
        if entree['id_staff'] == "0":
            id_staff = ""
            staff = ""
        else:
            id_staff = entree['id_staff']
            validateur = self.imports.users.donnees[id_staff]
            staff = validateur['nom'] + " " + validateur['prenom'][0] + "."
        return [entree['validation'], id_staff, staff]

    def __ref_client(self, annee, mois, classe, client, compte, article):
        """
        ajout de la référence et des valeurs issues du client
        :param annee: année de la transaction
        :param mois: mois de la transaction
        :param classe: classe de la transaction
        :param client: client de la transaction
        :param compte: compte de la transaction
        :param article: article de la transaction
        :return tableau contenant la référence et les valeurs du client
        """
        id_artsap = article['item-idsap']
        artsap = self.imports.artsap.donnees[id_artsap]
        plateforme = self.imports.plateforme
        if (classe['ref_fact'] == 'INT' and classe['avantage_HC'] == 'BONUS' and artsap['eligible'] == 'OUI' and
                compte['type_subside'] == "0" and plateforme['grille'] != "" and classe['grille'] == 'OUI'):
            icf = compte['id_compte']
        else:
            icf = "0"
        return [annee, mois, self.imports.version, icf, client['code'], client['code_sap'], client['abrev_labo'],
                client['id_classe'], classe['code_n'], classe['intitule']]

    def __util_proj(self, id_user, compte, flux):
        """
        ajout des valeurs issues de l'utilisateur et du projet (compte)
        :param id_user: id de l'utilisateur de la transaction
        :param compte: compte de la transaction
        :param flux: type de flux
        :return tableau contenant les valeurs de l'utilisateur et du projet
        """
        user = self.imports.users.donnees[id_user]
        return [user['id_user'], user['sciper'], user['nom'], user['prenom'], compte['id_compte'], compte['numero'],
                compte['intitule'], compte['exploitation'], flux]

    def __art_plate(self, article, code_k, texte_k, texte2_k):
        """
        ajout des valeurs issues de l'article et de la plateforme
        :param article: article de la transaction
        :param code_k: code catégorie
        :param texte_k: texte catégorie
        :param texte2_k: texte 2 catégorie
        :return tableau contenant les valeurs de l'article et de la plateforme
        """
        plateforme = self.imports.plateforme
        return [article['item-id'], code_k, texte_k, texte2_k, article['item-nbr'], article['item-name'],
                article['item-unit'], article['item-idsap'], article['item-codeD'], article['item-flag-usage'],
                article['item-flag-conso'], article['item-eligible'], article['item-order'], article['item-labelcode'],
                article['item-extra'], article['platf-code'], plateforme['code_p'], plateforme['abrev_plat']]

    def __subsides(self, transact, article):
        """
        ajout des valeurs issues des subsides
        :param transact: transaction
        :param article: article de la transaction
        :return tableau contenant les valeurs de subsides
        """
        id_compte = transact['up'][4]
        compte = self.imports.comptes.donnees[id_compte]
        id_classe = transact['rc'][7]
        montant = transact['val'][4]
        id_machine = transact['ope'][4]
        date = transact['trans'][0]
        validation = transact['trans'][2]
        type_s = compte['type_subside']
        result = ["", "", "", "", "", 0, 0, 0, 0, 0]
        if type_s != "0":
            if self.imports.edition.annee == transact['rc'][0] and self.imports.edition.mois == transact['rc'][1]:
                if type_s in self.imports.subsides.donnees.keys():
                    subside = self.imports.subsides.donnees[type_s]
                    result[0] = subside['type']
                    result[1] = subside['intitule']
                    result[2] = subside['debut']
                    result[3] = subside['fin']
                    result[4] = "NO"
                    if validation == "1":
                        plaf = type_s + article['platf-code'] + article['item-idsap']
                        if plaf in self.imports.plafonds.donnees.keys():
                            plafond = self.imports.plafonds.donnees[plaf]
                            result[5] = plafond['pourcentage']
                            result[6] = plafond['max_compte']
                            result[7] = plafond['max_mois']
                            if subside['debut'] == "NULL" or subside['debut'] <= date:
                                if subside['fin'] == "NULL" or subside['fin'] >= date:
                                    if type_s in self.imports.cles.donnees.keys():
                                        dict_s = self.imports.cles.donnees[type_s]
                                        if self.__check_id_classe(dict_s, id_classe, compte['code_client'], id_machine):
                                            result[4] = "YES"
                                            cg_id = compte['id_compte'] + article['platf-code'] + article['item-idsap']
                                            if cg_id in self.imports.grants.donnees.keys():
                                                grant = self.imports.grants.donnees[cg_id]['subsid-alrdygrant']
                                            else:
                                                grant = 0
                                            if cg_id in self.comptabilises.keys():
                                                comptabilise = self.comptabilises[cg_id]['subsid-alrdygrant']
                                            else:
                                                comptabilise = 0
                                            res_compte = plafond['max_compte'] - (grant + comptabilise)
                                            res_mois = plafond['max_mois'] - comptabilise
                                            res = max(min(res_compte, res_mois), 0)
                                            max_mo = round(montant * plafond['pourcentage'] / 100, 2)
                                            mo = min(max_mo, res)
                                            if cg_id not in self.comptabilises.keys():
                                                self.comptabilises[cg_id] = {'proj-id': compte['id_compte'],
                                                                             'platf-code': article['platf-code'],
                                                                             'item-idsap': article['item-idsap'],
                                                                             'subsid-alrdygrant': mo}
                                            else:
                                                self.comptabilises[cg_id]['subsid-alrdygrant'] = \
                                                    self.comptabilises[cg_id]['subsid-alrdygrant'] + mo
                                            result[8] = res
                                            result[9] = mo
            else:
                result[4] = "N/A"
        return result

    @staticmethod
    def __check_id_classe(dict_s, id_classe, code_client, id_machine):
        """
        vérifie si les clés subsides contiennent le code N, ou 0
        :param dict_s: dict pour le type
        :param id_classe: id_classe à vérifier
        :param code_client: code client à vérifier
        :param id_machine: machine à vérifier

        """
        if "0" in dict_s:
            if Transactions3.__check_client(dict_s, "0", code_client, id_machine):
                return True
        if id_classe in dict_s:
            if Transactions3.__check_client(dict_s, id_classe, code_client, id_machine):
                return True
        return False

    @staticmethod
    def __check_client(dict_p, id_classe, code_client, id_machine):
        """
        vérifie si les clés subsides contiennent le code client, ou 0
        :param dict_p: dict pour la plateforme
        :param id_classe: id classe sélectionné ou 0
        :param code_client: code client à vérifier
        :param id_machine: machine à vérifier
        """
        dict_n = dict_p[id_classe]
        if "0" in dict_n:
            if Transactions3.__check_machine(dict_n, "0", id_machine):
                return True
        if code_client in dict_n:
            if Transactions3.__check_machine(dict_n, code_client, id_machine):
                return True
        return False

    @staticmethod
    def __check_machine(dict_n, client, id_machine):
        """
        vérifie si les clés subsides contiennent l'id machine, ou 0
        :param dict_n: dict pour le code N
        :param client: client sélectionné ou 0
        :param id_machine: machine à vérifier
        """
        dict_c = dict_n[client]
        if "0" in dict_c:
            return True
        if id_machine in dict_c:
            return True
        return False

    @staticmethod
    def __put_in_transacts(transacts, ref_client, ope, util_proj, art, trans, val):
        """
        rajoute une ligne de transaction (avant tri chronologique et traitement des subsides)
        :param transacts: tableau des transactions
        :param ref_client: référence et valeurs issues du client
        :param ope: valeurs issues de l'opérateur
        :param util_proj: valeurs issues de l'utilisateur et du projet
        :param art: valeurs issues de l'article et de la plateforme
        :param trans: valeurs de transaction
        :param val: valeurs d'évaluation
        """
        fact_date = ref_client[0] + ref_client[1]
        if fact_date not in transacts.keys():
            transacts[fact_date] = {}
        if trans[0] not in transacts[fact_date].keys():
            transacts[fact_date][trans[0]] = []
        transacts[fact_date][trans[0]].append({'rc': ref_client, 'ope': ope, 'up': util_proj, 'art': art,
                                               'trans': trans, 'val': val})
