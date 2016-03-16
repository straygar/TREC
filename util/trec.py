import subprocess
from django.conf import settings
import os

_wantedValues = ["P_10", "P_20", "map"]

def _getTrecExec():
    return os.path.join(settings.BASE_DIR, "trec_eval")

def getRating(qrels_path, run_path):
    tempOutput = subprocess.check_output([_getTrecExec(), qrels_path, run_path])
    returnDict = {}
    for value in tempOutput.split("\n"):
        print value
        tempArray = value.strip().split("\t")
        identifier = tempArray[0].strip()
        if identifier in _wantedValues:
            returnDict[identifier] = float(tempArray[2].strip())
    return returnDict
