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

arguments = docopt(__doc__)

if arguments["--sansgraphiques"]:
    Outils.interface_graphique(False)

if arguments["--entrees"]:
    dossier_data = arguments["--entrees"]
else:
    dossier_data = Outils.choisir_dossier()
dossier_source = DossierSource(dossier_data)
try:
    start_time = time.time()

    Outils.affiche_message("OK !!! (" + str(datetime.timedelta(seconds=(time.time() - start_time))).split(".")[0] + ")")
except Exception as e:
    Outils.fatal(traceback.format_exc(), "Erreur imprévue :\n")
