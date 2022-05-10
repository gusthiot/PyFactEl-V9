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
                      Sommes)
from module_b import (GrantedNew,
                      NumeroNew,
                      Details,
                      AnnexeSubsides,
                      BilanSubsides,
                      Transactions2New)
from module_a import (VersionNew,
                      Modifications,
                      Annexe,
                      Transactions1,
                      BilanFactures,
                      Pdfs)
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

        # Module D
        imports = Imports(dossier_source)
        articles = Articles(imports)
        tarifs = Tarifs(imports)
        articles.csv(DossierDestination(imports.chemin_prix))
        tarifs.csv(DossierDestination(imports.chemin_prix))
        transactions3 = Transactions3(imports, articles, tarifs)
        transactions3.csv(DossierDestination(imports.chemin_bilans))

        # Module C
        sommes = Sommes(imports, transactions3)
        usr_lab = UserLaboNew(imports, transactions3, sommes.par_user)
        usr_lab.csv(DossierDestination(imports.chemin_out))
        sommes_ul = SommesUL(usr_lab, imports)
        bil_use = BilanUsages(imports, transactions3, sommes.par_item)
        bil_use.csv(DossierDestination(imports.chemin_bilans))
        bil_conso = BilanConsos(imports, transactions3, sommes.par_projet)
        bil_conso.csv(DossierDestination(imports.chemin_bilans))
        stat_nb_user = StatNbUser(imports, sommes_ul.par_ul)
        stat_nb_user.csv(DossierDestination(imports.chemin_bilans))
        stat_user = StatUser(imports, transactions3, sommes.par_user)
        stat_user.csv(DossierDestination(imports.chemin_bilans))
        stat_cli = StatClient(imports, transactions3, sommes_ul.par_ul, sommes.par_client)
        stat_cli.csv(DossierDestination(imports.chemin_bilans))
        stat_mach = StatMachine(imports, transactions3, sommes.par_machine)
        stat_mach.csv(DossierDestination(imports.chemin_bilans))

        # Module B
        new_grants = GrantedNew(imports, transactions3)
        new_grants.csv(DossierDestination(imports.chemin_out))
        new_numeros = NumeroNew(imports, transactions3)
        new_numeros.csv(DossierDestination(imports.chemin_out))
        ann_dets = Details(imports, transactions3, sommes.par_client, new_numeros)
        ann_subs = AnnexeSubsides(imports, transactions3, sommes.par_client, ann_dets.csv_fichiers)
        bil_subs = BilanSubsides(imports, transactions3, sommes.par_client)
        bil_subs.csv(DossierDestination(imports.chemin_bilans))
        new_transactions2 = Transactions2New(imports, transactions3, sommes.par_client, new_numeros)
        new_transactions2.csv(DossierDestination(imports.chemin_bilans))

        # Module A
        new_versions = VersionNew(imports, new_transactions2)
        new_versions.csv(DossierDestination(imports.chemin_out))
        modifications = Modifications(imports, new_versions)
        modifications.csv(DossierDestination(imports.chemin_version))
        annexes = Annexe(imports, new_transactions2, new_versions, ann_subs.csv_fichiers)
        Chemin.csv_files_in_zip(annexes.csv_fichiers, imports.chemin_cannexes)
        transactions1 = Transactions1(imports, new_transactions2, new_versions)
        transactions1.csv(DossierDestination(imports.chemin_bilans))
        bil_facts = BilanFactures(imports, transactions1)
        bil_facts.csv(DossierDestination(imports.chemin_bilans))
        # if Latex.possibles():
        #     pdfs = Pdfs(imports, new_transactions2, new_versions)

        Interface.affiche_message("OK !!! (" +
                                  str(datetime.timedelta(seconds=(time.time() - start_time))).split(".")[0] + ")")
    else:
        Interface.affiche_message("Carnet d'ordre introuvable")
except Exception as e:
    Interface.fatal(traceback.format_exc(), "Erreur imprévue :\n")
