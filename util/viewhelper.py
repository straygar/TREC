from django.shortcuts import render, get_object_or_404

def deleteFormGeneric(request, template, model, id, item_display_name, returnUrl):
    temp_object = get_object_or_404(model, id=id)
    deleted = False
    fail = False
    if request.method == "POST":
        try:
            temp_object.delete()
            deleted = True
        except:
            fail = True
    context_dict = {}
    context_dict["deleted"] = deleted
    context_dict["fail"] = fail
    context_dict["element"] = item_display_name
    context_dict["element_name"] = temp_object.title
    context_dict["element_desc"] = temp_object.description
    context_dict["url"] = request.get_full_path()
    context_dict["returnUrl"] = returnUrl
    return render(request, template, context_dict)


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
    context_dict["retUrl"] = request.get_full_path()
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
    contextDict["retUrl"] = request.get_full_path()
    return render(request, template, contextDict)