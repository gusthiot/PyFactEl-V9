# This Python file uses the following encoding: utf-8

"""
Fichier principal à lancer pour faire tourner le logiciel

Usage:
  main.py [options]

Options:

  -h   --help              Affiche le présent message
  --entrees <chemin>       Chemin des fichiers d'entrée
  --sansgraphiques         Pas d'interface graphique
"""
import datetime
import time
import traceback
from docopt import docopt
from core import (Interface,
                  Chemin,
                  DossierSource,
                  DossierDestination,
                  ErreurConsistance,
                  Latex)
from module_d import (Articles,
                      Tarifs,
                      Transactions3)
from module_c import (UserLaboNew,
                      BilanUsages,
                      BilanConsos,
                      StatMachine,
                      StatNbUser,
                      StatUser,
                      StatClient,
                      SommesUL,
                      Sommes3)
from module_b import (GrantedNew,
                      NumeroNew,
                      Details,
                      AnnexeSubsides,
                      BilanSubsides,
                      BilanAnnules,
                      Transactions2New)
from module_a import (VersionNew,
                      Sommes2,
                      Sommes1,
                      Modifications,
                      Annexe,
                      Transactions1,
                      BilanFactures,
                      Pdfs,
                      Journal,
                      Facture,
                      Total,
                      Ticket)
from imports import (Edition,
                     Imports)

arguments = docopt(__doc__)

if arguments["--sansgraphiques"]:
    Interface.interface_graphique(False)

if arguments["--entrees"]:
    dossier_data = arguments["--entrees"]
else:
    dossier_data = Interface.choisir_dossier()
dossier_source = DossierSource(dossier_data)
try:
    if Chemin.existe(Chemin.chemin([dossier_data, Edition.nom_fichier])):
        start_time = time.time()

        imports = Imports(dossier_source)

        # Module D
        articles = Articles(imports)
        tarifs = Tarifs(imports)
        if imports.version == 0:
            articles.csv(DossierDestination(imports.chemin_prix))
            tarifs.csv(DossierDestination(imports.chemin_prix))
        else:
            if not Chemin.existe(Chemin.chemin([imports.chemin_prix, articles.nom]), False):
                Interface.fatal(ErreurConsistance(), "le fichier " + articles.nom + " est censé exister !")
            if not Chemin.existe(Chemin.chemin([imports.chemin_prix, tarifs.nom]), False):
                Interface.fatal(ErreurConsistance(), "le fichier " + tarifs.nom + " est censé exister !")
        transactions_3 = Transactions3(imports, articles, tarifs)
        transactions_3.csv(DossierDestination(imports.chemin_bilans))

        # Module C
        sommes_3 = Sommes3(imports, transactions_3)
        usr_lab = UserLaboNew(imports, transactions_3, sommes_3.par_user)
        usr_lab.csv(DossierDestination(imports.chemin_out))
        sommes_ul = SommesUL(usr_lab, imports)
        bil_use = BilanUsages(imports, transactions_3, sommes_3.par_item)
        bil_use.csv(DossierDestination(imports.chemin_bilans))
        bil_conso = BilanConsos(imports, transactions_3, sommes_3.par_projet)
        bil_conso.csv(DossierDestination(imports.chemin_bilans))
        stat_nb_user = StatNbUser(imports, sommes_ul.par_ul)
        stat_nb_user.csv(DossierDestination(imports.chemin_bilans))
        stat_user = StatUser(imports, transactions_3, sommes_3.par_user)
        stat_user.csv(DossierDestination(imports.chemin_bilans))
        stat_cli = StatClient(imports, sommes_ul.par_ul, sommes_3.par_client)
        stat_cli.csv(DossierDestination(imports.chemin_bilans))
        stat_mach = StatMachine(imports, transactions_3, sommes_3.par_machine)
        stat_mach.csv(DossierDestination(imports.chemin_bilans))

        # Module B
        new_grants = GrantedNew(imports, transactions_3)
        new_grants.csv(DossierDestination(imports.chemin_out))
        new_numeros = NumeroNew(imports, transactions_3)
        new_numeros.csv(DossierDestination(imports.chemin_out))
        details = Details(imports, transactions_3, sommes_3.par_client, new_numeros)
        ann_subs = AnnexeSubsides(imports, sommes_3.par_client, details.csv_fichiers)
        bil_subs = BilanSubsides(imports, transactions_3, sommes_3.par_client)
        bil_subs.csv(DossierDestination(imports.chemin_bilans))
        bil_annule = BilanAnnules(imports, sommes_3.par_client)
        bil_annule.csv(DossierDestination(imports.chemin_bilans))
        new_transactions_2 = Transactions2New(imports, transactions_3, sommes_3.par_client, new_numeros)
        new_transactions_2.csv(DossierDestination(imports.chemin_bilans))

        # Module A
        sommes_2 = Sommes2(new_transactions_2)
        new_versions = VersionNew(imports, new_transactions_2, sommes_2)
        new_versions.csv(DossierDestination(imports.chemin_out))
        modifications = Modifications(imports, new_versions)
        modifications.csv(DossierDestination(imports.chemin_version))
        if imports.version > 0:
            journal = Journal(imports, new_versions, new_transactions_2)
            journal.csv(DossierDestination(imports.chemin_bilans))
        annexes = Annexe(imports, new_transactions_2, sommes_2, ann_subs.csv_fichiers)
        transactions_1 = Transactions1(imports, new_transactions_2, sommes_2, new_versions)
        transactions_1.csv(DossierDestination(imports.chemin_bilans))
        sommes_1 = Sommes1(transactions_1)
        bil_facts = BilanFactures(imports, transactions_1, sommes_1)
        bil_facts.csv(DossierDestination(imports.chemin_bilans))
        total = Total(imports, transactions_1, sommes_1, annexes.csv_fichiers)
        Chemin.csv_files_in_zip(total.csv_fichiers, imports.chemin_cannexes)
        if Latex.possibles():
            pdfs = Pdfs(imports, new_transactions_2, sommes_2, new_versions)
        factures = Facture(imports, new_versions, sommes_1)
        if imports.edition.filigrane == "":
            factures.csv(DossierDestination(imports.chemin_version))
        tickets = Ticket(imports, factures, sommes_1)
        tickets.creer_html(DossierDestination(imports.chemin_version))

        Interface.affiche_message("OK !!! (" +
                                  str(datetime.timedelta(seconds=(time.time() - start_time))).split(".")[0] + ")")
    else:
        Interface.affiche_message("Carnet d'ordre introuvable")
except Exception as e:
    Interface.fatal(traceback.format_exc(), "Erreur imprévue :\n")
