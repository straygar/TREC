import datetime
from main.models import Track

def convertDate(dateStr):
    return datetime.datetime.strptime(dateStr, "%Y-%m-%d")

def convertFloat(floatStr):
    return float(floatStr)

def convertTrack(trackStr):
    return Track.objects.get(title=trackStr)

def getOrDefault(dataStr, callFunction):
    if dataStr is None or len(dataStr.strip()) == 0:
        return None
    else:
        return callFunction(dataStr)