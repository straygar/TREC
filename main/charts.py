def chartShowTask(request):
	context_dict ={}
	myresearcher = get_object_or_404(Researcher, user=request.user)
	track_list = Run.objects.filter(researcher=researcher__user_username).values_list("task", flat=True)
	return render(request, "main/viewProfile.html"track_list)