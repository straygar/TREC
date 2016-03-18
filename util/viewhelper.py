from django.shortcuts import render, get_object_or_404

def editFormGeneric(request, template, model, formType, id):
    valid = False
    error = False
    currentElement = get_object_or_404(model,id=id)
    context_dict = {}
    if request.method == "POST":
        form = formType(request.POST, instance = currentElement)
        if form.is_valid():
            form.save()
            valid = True
        else:
            error = True
    else:
        form = formType(instance = currentElement)

    context_dict["form"] = form
    context_dict["valid"] = valid
    context_dict["error"] = error
    context_dict["new"] = False
    context_dict["title"] = currentElement.title
    return render(request, template, context_dict)

def uploadFormGeneric(request, template, formType, extraCallable, useFiles = False):
    contextDict = {}
    valid = False
    error = False
    if request.method == "GET":
        upl_form = formType()
    else:
        if not useFiles:
            upl_form = formType(data=request.POST)
        else:
            upl_form = formType(request.POST, request.FILES)
        if upl_form.is_valid():
            temp_data = upl_form.save(commit=False)
            # Extra processing before saving. Can be none if not required
            if extraCallable is not None:
                extraCallable(temp_data, upl_form)
            temp_data.save()
            valid = True
        else:
            error = True
    contextDict["form"] = upl_form
    contextDict["valid"] = valid
    contextDict["error"] = error
    contextDict["new"] = True
    return render(request, template, contextDict)