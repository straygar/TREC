from main.models import Researcher

def includeProfile(request):
    if request.user.is_authenticated():
        researcher = Researcher.objects.filter(user=request.user)
        if researcher is not None:
            if len(researcher) == 1:
                return {"userProfileObject":researcher[0]}

    return {}