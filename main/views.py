from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.forms import RunForm

@login_required
def uploadRun(request):
    contextDict = {}
    if request.method == "GET":
        upl_form = RunForm()
    else:
        upl_form = RunForm(data=request.POST)
        if upl_form.is_valid():
            upl_form.save(commit=True)
    contextDict["form"] = upl_form
    return render(request, "main/uploadRun.html", contextDict)