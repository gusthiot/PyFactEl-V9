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
from module_b import (Transactions2New)
from module_a import (VersionNew,
                      Sommes2,
                      Sommes1,
                      Modifications,
                      Annexe,
                      Transactions1,
                      BilanFactures,
                      Pdfs,
                      Facture,
                      Total,
                      Ticket)
from imports import (Edition,
                     ImportsA)

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

        imports = ImportsA(dossier_source)

        new_transactions_2 = Transactions2New(imports)
        new_transactions_2.csv(DossierDestination(imports.chemin_bilans))

        # Module A
        sommes_2 = Sommes2(new_transactions_2)
        new_versions = VersionNew(imports, new_transactions_2, sommes_2)
        new_versions.csv(DossierDestination(imports.chemin_out))
        modifications = Modifications(imports, new_versions)
        modifications.csv(DossierDestination(imports.chemin_version))
        annexes = Annexe(imports, new_transactions_2, sommes_2)
        transactions_1 = Transactions1(imports, new_transactions_2, sommes_2)
        transactions_1.csv(DossierDestination(imports.chemin_bilans))
        sommes_1 = Sommes1(transactions_1)
        bil_facts = BilanFactures(imports, transactions_1, sommes_1)
        bil_facts.csv(DossierDestination(imports.chemin_bilans))
        total = Total(imports, transactions_1, sommes_1, annexes.csv_fichiers)
        Chemin.csv_files_in_zip(annexes.csv_fichiers, imports.chemin_cannexes)
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
