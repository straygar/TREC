import datetime

def convertDate(dateStr):
    return datetime.datetime.strptime(dateStr, "%Y-%m-%d")

def getOrDefault(dataStr, callFunction):
    if dataStr is None or len(dataStr.strip()) == 0:
        return None
    else:
        return callFunction(dataStr)