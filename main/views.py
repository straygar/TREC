from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_permission_decorator

from main.models import Task, Run, Researcher, Genre
from main.forms import RunForm, RunFileForm, UserForm, UserProfileForm, TaskForm, TrackForm, GenreForm, ReturnUrlForm

from django.contrib.auth.models import User
from django.template import RequestContext

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from util import trec
from trec import roles

def index(request):
    context_dict = {}
    run_list = Run.objects.all()[:10]
    context_dict = { 'runs' : run_list}

    return render(request, 'main/index.html', context_dict)

def browse(request):
    return render(request, 'main/browse.html')

@login_required
def uploadRun(request):
    contextDict = {}
    finish = False
    fail = False
    results = {}
    if request.method == "GET":
        upl_form = RunForm()
        upl_file_form = RunFileForm()
    else:
        upl_form = RunForm(request.POST)
        upl_file_form = RunFileForm(request.POST, request.FILES)
        if upl_file_form.is_valid() and upl_form.is_valid():
            file_upload = upl_file_form.save(commit=True)
            temp_data = upl_form.save(commit=False)
            temp_data.result_file = file_upload
            temp_data.researcher = request.user
            temp_data.task = upl_form.cleaned_data["task"]
            try:
                results = trec.getRating(temp_data.task.judgement_file.path, file_upload.result_file.path)
                temp_data.p10 = results["P_10"]
                temp_data.p20 = results["P_20"]
                temp_data.map = results["map"]
                temp_data.save()
                finish = True
            except:
                fail = True

    contextDict["form"] = upl_form
    contextDict["form_file"] = upl_file_form
    contextDict["finish"] = finish
    contextDict["fail"] = fail
    contextDict["results"] = results
    return render(request, "main/uploadRun.html", contextDict)

@has_permission_decorator("edit_tracks")
def uploadGenre(request):
    contextDict = {}
    posted = False
    retUrl = ""
    if request.method == "GET":
        upl_form = GenreForm()
        retForm = ReturnUrlForm(initial={"url":request.META.get("HTTP_REFERER")})
    else:
        upl_form = GenreForm(data=request.POST)
        if upl_form.is_valid():
            upl_form.save(commit=True)
            posted = True
        retForm = ReturnUrlForm(data=request.POST)
        if retForm.is_valid():
            retUrl = retForm.cleaned_data["url"]
    contextDict["form"] = upl_form
    contextDict["posted"] = posted
    contextDict["retUrl"] = retUrl
    contextDict["retForm"] = retForm
    return render(request, "main/uploadGenre.html", contextDict)

@has_permission_decorator("edit_tracks")
def uploadTask(request):
    contextDict = {}
    retUrl = ""
    if request.method == "GET":
        upl_form = TaskForm()
        retForm = ReturnUrlForm(initial={"url":request.META.get("HTTP_REFERER")})
    else:
        upl_form = TaskForm(request.POST, request.FILES)
        if upl_form.is_valid():
            temp_data = upl_form.save(commit=False)
            temp_data.track = upl_form.cleaned_data["track"]
            temp_data.save()
        retForm = ReturnUrlForm(data=request.POST)
        if retForm.is_valid():
            retUrl = retForm.cleaned_data["url"]
    contextDict["form"] = upl_form
    contextDict["retUrl"] = retUrl
    contextDict["retForm"] = retForm
    return render(request, "main/uploadTask.html", contextDict)

@has_permission_decorator("edit_tracks")
def uploadTrack(request):
    contextDict = {}
    retUrl = ""
    if request.method == "GET":
        upl_form = TrackForm()
        retForm = ReturnUrlForm(initial={"url":request.META.get("HTTP_REFERER")})
    else:
        upl_form = TrackForm(data=request.POST)
        if upl_form.is_valid():
            temp_data = upl_form.save(commit=False)
            temp_data.genre = upl_form.cleaned_data["genre"]
            temp_data.save()
        retForm = ReturnUrlForm(data=request.POST)
        if retForm.is_valid():
            retUrl = retForm.cleaned_data["url"]
    contextDict["form"] = upl_form
    contextDict["retUrl"] = retUrl
    contextDict["retForm"] = retForm
    return render(request, "main/uploadTrack.html", contextDict)

def register(request):
    context_dict = {}
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            roles.Researcher.assign_role_to_user(user)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()
            registered = True

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict['user_form'] = user_form
    context_dict['profile_form']= profile_form
    context_dict['registered'] = registered

    return render(request,'main/register.html',context_dict)


@login_required
def edit_profile(request):
     # Request the context.
    context = RequestContext(request)
    context_dict = {}
    old_profile=Researcher.objects.get(user=request.user)

    # If HTTP POST, we wish to process form data and create an account.
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)

        # Two valid forms?
        if profile_form.is_valid():

            # We'll be setting values for the instance ourselves, so commit=False prevents Django
            # from saving the instance automatically.
            profile = profile_form.save(commit=False)
            profile.user = request.user

            # Profile picture supplied? If so, we put it in the new UserProfile.
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            # Now we save the model instance!
            profile.save()

            return HttpResponseRedirect('/main/profile/')


        # Invalid form(s) - just print errors to the terminal.
        else:
            print profile_form.errors

    # Not a HTTP POST, so we render the two ModelForms to allow a user to input their data.
    else:
        profile_form = UserProfileForm(instance=old_profile)

    context_dict['profile_form']= profile_form

    # Render and return!
    return render_to_response(
        'main/edit_profile.html',
        context_dict,
        context)

def user_login(request):
    # Obtain our request's context.
    context = RequestContext(request)
    context_dict = {}

    # If HTTP POST, pull out form data and process it.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # A valid user logged in?
        if user is not None:
            # Check if the account is active (can be used).
            # If so, log the user in and redirect them to the homepage.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
            # The account is inactive; tell by adding variable to the template context.
            else:
                context_dict['disabled_account'] = True
                return render_to_response('main/login.html', context_dict, context)
        # Invalid login details supplied!
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('main/login.html', context_dict, context)

    # Not a HTTP POST - most likely a HTTP GET. In this case, we render the login form for the user.
    else:
        return render_to_response('main/login.html', context_dict, context)


def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/main/')


@login_required
def profile(request):
    context = RequestContext(request)
    context_dict={}

    u = User.objects.get(username=request.user)
    up = Researcher.objects.get(user=u)
    print up

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('main/profile.html', context_dict, context)

def about(request):
    return render(request,'main/about.html')

def viewRun(request, runid):
    return render(request, "main/viewRun.html", {"run":Run.objects.get(id=runid)})

def viewTrack(request, trackid):
    pass

def editTrack(request, trackid):
    pass

def viewTask(request, taskid):
    pass

def editTask(request, taskid):
    pass
