import datetime
from main.models import Task, Track, Genre, Researcher
from django.contrib.auth.models import User

def convertDate(dateStr):
    return datetime.datetime.strptime(dateStr, "%Y-%m-%d")

def convertFloat(floatStr):
    return float(floatStr)

def getOrDefault(dataStr, callFunction):
    if dataStr is None or len(dataStr.strip()) == 0:
        return None
    else:
        return callFunction(dataStr)

def checkNotAllNull(data):
    for item in data:
        if item is not None:
            return True
    return False