from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.forms import RunForm
from main.models import Task

@login_required
def uploadRun(request):
    contextDict = {}
    if request.method == "GET":
        upl_form = RunForm()
    else:
        upl_form = RunForm(request.POST, request.FILES)
        if upl_form.is_valid():
            temp_data = upl_form.save(commit=False)
            temp_data.result_file = request.FILES["result_file"]
            temp_data.researcher = request.user
            temp_data.task = Task.objects.all()[0]
            temp_data.map = 2
            temp_data.p10 = 1
            temp_data.p20 = 4
            temp_data.save()
        else:
            print upl_form.errors
    contextDict["form"] = upl_form
    return render(request, "main/uploadRun.html", contextDict)