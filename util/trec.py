import subprocess
from django.conf import settings
import os
from django.db.models import Avg, Max

_wantedValues = ["P_10", "P_20", "map"]

def _getTrecExec():
    return os.path.join(settings.BASE_DIR, "trec_eval")

def getRating(qrels_path, run_path):
    tempOutput = subprocess.check_output([_getTrecExec(), qrels_path, run_path])
    returnDict = {}
    for value in tempOutput.split("\n"):
        tempArray = value.strip().split("\t")
        identifier = tempArray[0].strip()
        if identifier in _wantedValues:
            returnDict[identifier] = float(tempArray[2].strip())
    return returnDict

def getMaximums(run_list):
    returnData = []
    field_names = ("p10","p20","map",)
    for field in field_names:
        temp = run_list.aggregate(Avg(field)).values()[0]
        if temp is not None:
            returnData.append((field + " Average", temp,))
    for field in field_names:
        temp = run_list.aggregate(Max(field)).values()[0]
        if temp is not None:
            returnData.append((field + " Maximum", temp,))
    return returnData
