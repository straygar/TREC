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