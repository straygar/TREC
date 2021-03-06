import datetime
from main.models import Task, Track, Genre, Researcher
from django.contrib.auth.models import User
import json

def convertDate(dateStr):
    return datetime.datetime.strptime(dateStr, "%d-%m-%Y")

def convertFloat(floatStr):
    return float(floatStr)

def getOrDefault(dataStr, callFunction):
    if dataStr is None or len(dataStr.strip()) == 0:
        return None
    else:
        return callFunction(dataStr)

def checkNotAllNull(data):
    for item in data:
        print item
        if item is not None:
            return True
    return False

def getJsonResponse(request, value, model, fieldName, param="query", maxResults=6):
    query = request.GET.get(param, None)
    if query is None or len(query.strip()) == 0:
        returnData = json.dumps({})
    else:
        fields = model.objects.filter(**{fieldName:query}).values_list(value, flat=True).distinct()
        returnData = json.dumps(list(fields)[:maxResults]) # Required to conver to a List and not a ValuesListQuerySet
    return returnData