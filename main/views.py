from django.shortcuts import render, render_to_response, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_permission_decorator

from main.models import Task, Track, Run, Researcher, Genre
from main.forms import RunForm, RunFileForm, UserForm, UserProfileForm, TaskForm, TrackForm, GenreForm, ReturnUrlForm, BrowseForm

from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils import timezone

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from util import trec, viewhelper
from util.dataparser import *
from trec import roles

import json
from django.core.serializers.json import DjangoJSONEncoder

def index(request):
    context_dict = {}

    best_list = Run.objects.all().order_by('p10')
    context_dict["best"] = best_list
    recent_list = Run.objects.all().order_by('-datetime')
    context_dict["recent"] = recent_list

    return render(request, 'main/index.html', context_dict)

def browse(request):
    contextDict = {}
    accepted = False
    if request.method == "GET":
        browse_form = BrowseForm()
    else:
        browse_form = BrowseForm(request.POST)
        if browse_form.is_valid():
            selection = browse_form.save(commit=False)
            accepted = True
            contextDict["task"] = browse_form.cleaned_data["task"]
            #contextDict["track"] = browse_form.cleaned_data["track"]
            run_list = Run.objects.filter(task = browse_form.cleaned_data["task"])
            contextDict["runs"] = run_list

    contextDict["form"] = browse_form
    contextDict["accepted"] = accepted

    return render(request, 'main/browse.html', contextDict)

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
                run_list = Run.objects.filter(task=temp_data.task).order_by('p10')
                contextDict["runs"] = run_list
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
    return viewhelper.uploadFormGeneric(request, "main/uploadGenre.html", GenreForm, None)

@has_permission_decorator("edit_tracks")
def uploadTask(request):
    def extraCallable(data, form):
        data.track = form.cleaned_data["track"]
    return viewhelper.uploadFormGeneric(request, "main/uploadTask.html", TaskForm, extraCallable, True)

@has_permission_decorator("edit_tracks")
def uploadTrack(request):
    def extraCallable(data, form):
        data.genre = form.cleaned_data["genre"]
    return viewhelper.uploadFormGeneric(request, "main/uploadTrack.html", TrackForm, extraCallable)

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
    old_profile=get_object_or_404(Researcher, user=request.user)

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
    up = get_object_or_404(Researcher, user=u)
    print up

    #p10 = Run.objects.filter(researcher=request.user)[:5].values_list('p10')
    #p20 = Run.objects.filter(researcher=request.user)[:5].values_list('p10')
    #p10_json = json.dumps(list(p10),cls=DjangoJSONEncoder)
    #p20_json = json.dumps(list(p20),cls=DjangoJSONEncoder)

    r =  Run.objects.filter(researcher=request.user)[:1]

    context_dict['user'] = u
    context_dict['userprofile'] = up
    context_dict['run']=r

    return render_to_response('main/profile.html', context_dict, context)

def about(request):
    return render(request,'main/about.html')

def viewRun(request, runid):
    context_dict = {}
    context_dict["run"] = run_info = get_object_or_404(Run, id=runid)
    context_dict["profile"] = get_object_or_404(Researcher, user=run_info.researcher)
    return render(request, "main/viewRun.html", context_dict)

def viewTrack(request, trackid):
    track = get_object_or_404(Track, id=trackid)
    tasks = Task.objects.filter(track=track)
    context_dict = {}
    context_dict["track"] = track
    context_dict["tasks"] = tasks
    return render(request, "main/viewTrack.html", context_dict)

def editTrack(request, trackid):
    return viewhelper.editFormGeneric(request, "main/uploadTrack.html", Track, TrackForm, trackid)

def viewTask(request, taskid):
    return render(request, "main/viewTask.html", {"task":get_object_or_404(Task, id=taskid)})

def editTask(request, taskid):
    return viewhelper.editFormGeneric(request, "main/uploadTask.html", Task, TaskForm, taskid)

def search(request):
    error = False
    track = request.GET.get("track", None)
    task = request.GET.get("task", None)
    uploader_username = request.GET.get("username", None)
    uploader_name = request.GET.get("displayname", None)
    runtype = request.GET.get("runtype", None)
    genre = request.GET.get("genre", None)
    feedback_type = request.GET.get("feedback", None)
    map_min = request.GET.get("map_min", None)
    map_max = request.GET.get("map_max", None)
    p10_min = request.GET.get("p10_min", None)
    p10_max = request.GET.get("p10_max", None)
    p20_min = request.GET.get("p20_min", None)
    p20_max = request.GET.get("p20_max", None)
    date_min = request.GET.get("date_min", None)
    date_max = request.GET.get("date_max", None)
    filtered_objects = Run.objects.all()
    # Convert to the right data types
    try:
        date_min_c = getOrDefault(date_min, convertDate)
        date_max_c = getOrDefault(date_max, convertDate)
        p10_min_c = getOrDefault(p10_min, convertFloat)
        p10_max_c = getOrDefault(p10_max, convertFloat)
        p20_min_c = getOrDefault(p20_min, convertFloat)
        p20_max_c = getOrDefault(p20_max, convertFloat)
        map_min_c = getOrDefault(map_min, convertFloat)
        map_max_c = getOrDefault(map_max, convertFloat)
        track_c = getOrDefault(track, convertTrack)
        if date_min_c is not None:
            filtered_objects = filtered_objects.filter(datetime__gte=date_min_c)
        if date_max_c is not None:
            filtered_objects = filtered_objects.filter(datetime__lte=date_max_c)
        if p10_min_c is not None:
            filtered_objects = filtered_objects.filter(p10__gte=p10_min_c)
        if p10_max_c is not None:
            filtered_objects = filtered_objects.filter(p10__lte=p10_max_c)
        if p20_min_c is not None:
            filtered_objects = filtered_objects.filter(p20__gte=p20_min_c)
        if p20_max_c is not None:
            filtered_objects = filtered_objects.filter(p20__lte=p20_max_c)
        if map_min_c is not None:
            filtered_objects = filtered_objects.filter(map__gte=map_min_c)
        if map_max_c is not None:
            filtered_objects = filtered_objects.filter(map__lte=map_max_c)
    except:
        error = True

