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
from core import (Outils,
                  DossierSource,
                  DossierDestination)
from module_d import (Articles,
                      Tarifs,
                      Transactions3,
                      Sommes)
from module_c import (UserLaboNew,
                      BilanUsages,
                      BilanConsos,
                      StatMachine,
                      StatNbUser,
                      StatUser,
                      StatClient,
                      SommesUL)
from imports import (Edition,
                     Imports)

arguments = docopt(__doc__)

if arguments["--sansgraphiques"]:
    Outils.interface_graphique(False)

if arguments["--entrees"]:
    dossier_data = arguments["--entrees"]
else:
    dossier_data = Outils.choisir_dossier()
dossier_source = DossierSource(dossier_data)
try:
    if Outils.existe(Outils.chemin([dossier_data, Edition.nom_fichier])):
        start_time = time.time()
        # Module D
        imports = Imports(dossier_source)
        articles = Articles(imports)
        tarifs = Tarifs(imports)
        articles.csv(DossierDestination(imports.chemin_prix))
        tarifs.csv(DossierDestination(imports.chemin_prix))
        transactions = Transactions3(imports, imports.version, articles, tarifs)
        transactions.csv(DossierDestination(imports.chemin_bilans))
        sommes = Sommes(transactions)

        # Module C
        usr_lab = UserLaboNew(imports, transactions, sommes.par_user)
        usr_lab.csv(DossierDestination(imports.chemin_out))
        sommes_ul = SommesUL(usr_lab, imports)
        bil_use = BilanUsages(imports, transactions, sommes.par_item)
        bil_use.csv(DossierDestination(imports.chemin_bilans))
        bil_conso = BilanConsos(imports, transactions, sommes.par_projet)
        bil_conso.csv(DossierDestination(imports.chemin_bilans))
        stat_nb_user = StatNbUser(imports, sommes_ul.par_ul)
        stat_nb_user.csv(DossierDestination(imports.chemin_bilans))
        stat_user = StatUser(imports, transactions, sommes.par_user)
        stat_user.csv(DossierDestination(imports.chemin_bilans))
        stat_cli = StatClient(imports, transactions, sommes_ul.par_ul, sommes.par_client)
        stat_cli.csv(DossierDestination(imports.chemin_bilans))
        stat_mach = StatMachine(imports, transactions, sommes.par_machine)
        stat_mach.csv(DossierDestination(imports.chemin_bilans))

        # Module B

        Outils.affiche_message("OK !!! (" +
                               str(datetime.timedelta(seconds=(time.time() - start_time))).split(".")[0] + ")")
    else:
        Outils.affiche_message("Carnet d'ordre introuvable")
except Exception as e:
    Outils.fatal(traceback.format_exc(), "Erreur imprévue :\n")
