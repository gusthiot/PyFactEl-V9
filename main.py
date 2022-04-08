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
                  DossierSource)
from module_d import ModuleD
from imports import Edition

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
        ModuleD.run(dossier_source)
        Outils.affiche_message("OK !!! (" +
                               str(datetime.timedelta(seconds=(time.time() - start_time))).split(".")[0] + ")")
    else:
        Outils.affiche_message("Carnet d'ordre introuvable")
except Exception as e:
    Outils.fatal(traceback.format_exc(), "Erreur imprévue :\n")
