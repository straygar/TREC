from django.shortcuts import render, render_to_response, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required

from main.models import Task, Track, Run, Researcher, Genre
from main.forms import RunForm, RunFileForm, UserForm, UserProfileForm,\
    TaskForm, TrackForm, GenreForm, ReturnUrlForm, BrowseTrackForm, BrowseTaskForm, BrowseTaskSortForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils import timezone

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from util import trec, viewhelper
from util.dataparser import *

import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from decimal import *

from chartit import *

def index(request):
    context_dict = {}

    best_list = Run.objects.all().order_by('-p10', '-p20', '-map')[:10]
    context_dict["best"] = best_list
    recent_list = Run.objects.all().order_by('-datetime')[:10]
    context_dict["recent"] = recent_list

    return render(request, 'main/index.html', context_dict)

def browse(request):
    contextDict = {}
    if request.method == "GET":
        browse_form = BrowseTrackForm()
    else:
        browse_form = BrowseTrackForm(request.POST)
        if browse_form.is_valid():
            track = browse_form.cleaned_data["track"]
            return HttpResponseRedirect(reverse("browseTrack", kwargs={"trackid":track.id}))
    contextDict["action_url"] = reverse("browse")
    contextDict["submit_msg"] = "Submit"
    contextDict["form"] = browse_form
    return render(request, 'main/browse.html', contextDict)

def browseTrack(request, trackid):
    contextDict = {}
    thisTrack = get_object_or_404(Track, id=trackid)
    sort_type = ""
    sort_order = ""
    if request.method == "GET":
        browse_form = BrowseTaskForm(track=thisTrack)
        sort_form = BrowseTaskSortForm()
    else:
        browse_form = BrowseTaskForm(request.POST, track=thisTrack)
        sort_form = BrowseTaskSortForm(data=request.POST)
        if browse_form.is_valid():
            if sort_form.is_valid():
                sort_type = sort_form.cleaned_data["sortOn"]
                sort_order = sort_form.cleaned_data["sortOrd"]
            returnUrl = reverse("browseComplete", kwargs={"taskid":browse_form.cleaned_data["task"].id})
            returnUrl += "?userRuns=" + str("my_tracks" in request.POST)
            returnUrl += "&pageSize=" + browse_form.cleaned_data["size"]
            if len(sort_type) != 0:
                returnUrl += "&Sort=" + sort_type.strip() + "&Order=" + sort_order.strip()
            return HttpResponseRedirect(returnUrl)
    contextDict["track"] = thisTrack
    contextDict["action_url"] = reverse("browseTrack", kwargs={"trackid":trackid})
    contextDict["submit_msg"] = "Browse runs for this task"
    contextDict["form"] = browse_form
    contextDict["sort_form"] = sort_form
    return render(request, 'main/browse.html', contextDict)

def browseComplete(request, taskid):
    reverseLookup = {"DA": "datetime",
                     "P1": "p10",
                     "P2": "p20",
                     "MA": "map",
                     "FT": "feedback_type",
                     "RT": "run_type",
                     "QT": "query_type",
                     "UO": "researcher__organization",
                     "UU": "researcher__user_username",
                     "UN": "researcher__display_name",
                     "TL": "name",}
    pageNo = request.GET.get("page", "1")
    pageSize = request.GET.get("pageSize", "10")
    errorSorting = False
    contextDict = {}
    userRunsRequested = False
    thisTask = get_object_or_404(Task, id=taskid)
    if request.user.is_authenticated():
        if request.GET.get('userRuns') == "True":
            userRunsRequested = True
    filtered_objects = Run.objects.filter(task__id=taskid)
    # Get averages BEFORE paginating and limiting results
    averages = trec.getMaximums(filtered_objects)
    if userRunsRequested:
        filtered_objects = filtered_objects.filter(researcher__user=request.user)
    try:
        if pageSize != "all":
            pageSize = int(pageSize)
        else:
            pageSize = filtered_objects.count()
    except:
        pageSize = 10
    sortType = request.GET.get('Sort')
    orderType = request.GET.get('Order')
    if orderType is not None:
        orderType = orderType.strip()
    else:
        orderType = "DE"
    if sortType is not None:
        sortType = sortType.strip()
    else:
        sortType = ""

    if len(sortType) > 0:
        if reverseLookup.has_key(sortType):
            sortStr = reverseLookup[sortType]
            if orderType == "DE":
                sortStr = "-" + sortStr
            filtered_objects = filtered_objects.order_by(sortStr)
        else:
            if sortType == "AL":
                if orderType == "DE":
                    filtered_objects = filtered_objects.order_by("-p10", "-p20", "-map")
                else:
                    filtered_objects = filtered_objects.order_by("p10", "p20", "map")
            else:
                errorSorting = True
    paginator = Paginator(filtered_objects, pageSize)
    try:
        page = paginator.page(pageNo)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    filtered_objects = page.object_list
    contextDict["averages"] = averages
    contextDict["errorSorting"] = errorSorting
    contextDict["task"] = thisTask
    contextDict["track"] = thisTask.track
    contextDict["user"] = request.user
    contextDict["runs"] = page
    contextDict["userRunsRequested"] = userRunsRequested
    contextDict["pageSize"] = pageSize
    cht = None
    # Don't show a graph if no results will be shown
    if len(filtered_objects) > 0:
        if request.user.is_authenticated():
            # Need to get the IDs in our current list since Django does not allow to filter after slicing
            our_id = filtered_objects.values_list("id", flat=True)
            our_runs = Run.objects.filter(id__in=our_id)
            myRuns = our_runs.filter(researcher__user=request.user)
            otherRuns = our_runs.exclude(researcher__user=request.user)
        else:
            myRuns = []
            otherRuns = filtered_objects

        if len(myRuns) > 0:
            ds = DataPool(
               series=
                [{'options': {
                    'source': otherRuns},
                  'terms': [
                    'datetime',
                    'map',
                    'p10',
                    'p20']},
                 {'options': {
                    'source': myRuns},
                  'terms': [
                      {'your_datetime':'datetime'},
                      {'Your map':'map'},
                      {'Your p10':'p10'},
                      {'Your p20':'p20'}]}
                 ])
            cht = Chart(
            datasource = ds,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'datetime': [
                    'p10',
                    'p20',
                    'map'],
                    'your_datetime': [
                        'Your p10',
                        'Your p20',
                        'Your map'
                    ]
                  }}],
            chart_options =
              {'title': {
                   'text': 'P10, P20 and Map scores over time'},
               'xAxis': {
                    'title': {
                       'text': 'Date & time'},
                    'labels': {
                        'formatter':'formatter'
                    }},
                'tooltip': {
                    'formatter':'tooltipFormatter'
                },
               'yAxis': {
                   'title': {
                       'text': 'Score'
                   }}})
        else:
            ds = DataPool(
               series=
                [{'options': {
                    'source': otherRuns},
                  'terms': [
                    'datetime',
                    'map',
                    'p10',
                    'p20']}])
            cht = Chart(
            datasource = ds,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'datetime': [
                    'p10',
                    'p20',
                    'map'],
                  }}],
            chart_options =
              {'title': {
                   'text': 'P10, P20 and Map scores over time'},
               'xAxis': {
                    'title': {
                       'text': 'Date & time'},
                    'labels': {
                        'formatter':'formatter'
                    }},
                'tooltip': {
                    'formatter':'tooltipFormatter'
                },
               'yAxis': {
                   'title': {
                       'text': 'Score'
                   }
               }})
    if cht is not None:
        contextDict["chart"] = cht
    return render(request, 'main/browseTask.html', contextDict)

@login_required
def uploadRun(request):
    contextDict = {}
    finish = False
    fail = False
    results = {}
    averages = []
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
            temp_data.researcher = get_object_or_404(Researcher,user=request.user)
            temp_data.task = upl_form.cleaned_data["task"]
            try:
                results = trec.getRating(temp_data.task.judgement_file.path, file_upload.result_file.path)
                temp_data.p10 = results["P_10"]
                temp_data.p20 = results["P_20"]
                temp_data.map = results["map"]
                run_list = Run.objects.filter(task=temp_data.task).order_by('-p10', '-p20', '-map')[:10]
                averages = trec.getMaximums(run_list)
                contextDict["runs"] = run_list
                temp_data.save()
                finish = True
            except:
                fail = True
    contextDict["averages"] = averages
    contextDict["form"] = upl_form
    contextDict["form_file"] = upl_file_form
    contextDict["finish"] = finish
    contextDict["fail"] = fail
    contextDict["results"] = results
    contextDict["user"] = request.user
    return render(request, "main/uploadRun.html", contextDict)

@staff_member_required
def uploadGenre(request):
    return viewhelper.uploadFormGeneric(request, "main/uploadGenre.html", GenreForm, None)

@staff_member_required
def uploadTask(request):
    def extraCallable(data, form):
        data.track = form.cleaned_data["track"]
    return viewhelper.uploadFormGeneric(request, "main/uploadTask.html", TaskForm, extraCallable, True)

@staff_member_required
def uploadTrack(request):
    def extraCallable(data, form):
        data.genre = form.cleaned_data["genre"]
    return viewhelper.uploadFormGeneric(request, "main/uploadTrack.html", TrackForm, extraCallable)

@login_required
def viewProfile(request, userId):
    taskQuery = request.GET.get("task", None)
    this_user = get_object_or_404(User, id=userId)
    this_profile = get_object_or_404(Researcher, user=this_user)
    context_dict = {}
    if taskQuery is not None:
        thisTask = get_object_or_404(Task, id=taskQuery)
        Runs = Run.objects.filter(task=thisTask)
        myRuns = Runs.filter(researcher=this_profile)
        ds = DataPool(
               series=
                [{'options': {
                    'source': myRuns},
                  'terms': [
                    'datetime',
                    'map',
                    'p10',
                    'p20']}])
        cht = Chart(
            datasource = ds,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'datetime': [
                    'p10',
                    'p20',
                    'map'],
                  }}],
            chart_options =
              {'title': {
                   'text': 'P10, P20 and Map scores over time'},
               'xAxis': {
                    'title': {
                       'text': 'Date & time'},
                    'labels': {
                        'formatter':'formatter'
                    }},
                'tooltip': {
                    'formatter':'tooltipFormatter'
                },
               'yAxis': {
                   'title': {
                       'text': 'Score'
                   }
               }})
        context_dict["chart"] = cht
    runs = Run.objects.filter(researcher=this_profile).order_by("-datetime")[:5]
    myProfile = this_user == request.user
    taskList = Run.objects.filter(researcher=this_profile).values("task","task__title").distinct()
    context_dict["user"] = this_user
    context_dict["profile"] = this_profile
    context_dict["runs"] = runs
    context_dict["thisUser"] = myProfile
    context_dict["taskList"] = taskList
    return render(request, "main/viewProfile.html", context_dict)

def register(request):
    context_dict = {}
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
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
    context = RequestContext(request)
    context_dict = {}
    old_profile=get_object_or_404(Researcher, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            if 'profile_picture' in request.FILES:
                old_profile.profile_picture = request.FILES['profile_picture']
            old_profile.website = profile_form.cleaned_data["website"]
            old_profile.display_name = profile_form.cleaned_data["display_name"]
            old_profile.organization = profile_form.cleaned_data["organization"]
            old_profile.save()
            return HttpResponseRedirect(reverse("view_profile", kwargs={"userId":request.user.id}))
    else:
        profile_form = UserProfileForm(instance=old_profile)

    context_dict['profile_form']= profile_form

    return render_to_response(
        'main/edit_profile.html',
        context_dict,
        context)

def user_login(request):
    context = RequestContext(request)
    context_dict = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                context_dict['disabled_account'] = True
        else:
            context_dict['bad_details'] = True
    context_dict["regist_count"] = User.objects.count()
    context_dict["runs_count"] = Run.objects.count()
    context_dict["task_count"] = Task.objects.count()
    context_dict["runs_today"] = Run.objects.filter(datetime__gte=timezone.now().replace(hour=0, minute=0, second=0)).count()
    return render_to_response('main/login.html', context_dict, context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/main/')

def about(request):
    return render(request,'main/about.html')

def viewRun(request, runid):
    context_dict = {}
    context_dict["run"] = run_info = get_object_or_404(Run, id=runid)
    context_dict["profile"] = run_info.researcher
    return render(request, "main/viewRun.html", context_dict)

def viewTrack(request, trackid):
    track = get_object_or_404(Track, id=trackid)
    tasks = Task.objects.filter(track=track)
    context_dict = {}
    context_dict["track"] = track
    context_dict["tasks"] = tasks
    return render(request, "main/viewTrack.html", context_dict)

@staff_member_required
def editTrack(request, trackid):
    return viewhelper.editFormGeneric(request, "main/uploadTrack.html", Track, TrackForm, trackid)

@staff_member_required
def editGenre(request, genreid):
    return viewhelper.editFormGeneric(request, "main/uploadGenre.html", Genre, GenreForm, genreid)

def viewTask(request, taskid):
    runs = Run.objects.filter(task__id=taskid).order_by("-datetime")[:10]
    best_runs = Run.objects.filter(task__id=taskid).order_by('-p10', '-p20', '-map')[:10]
    return render(request, "main/viewTask.html", {"task":get_object_or_404(Task, id=taskid), "runs":runs, "best_runs":best_runs})

@staff_member_required
def editTask(request, taskid):
    return viewhelper.editFormGeneric(request, "main/uploadTask.html", Task, TaskForm, taskid, True)

def search(request):
    error = False
    context_dict = {}
    track = request.GET.get("track", None)
    task = request.GET.get("task", None)
    uploader_username = request.GET.get("username", None)
    uploader_name = request.GET.get("displayname", None)
    organization = request.GET.get("organization", None)
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
    name = request.GET.get("name", None)
    pageSize = request.GET.get("pageSize", "10")
    pageNo = request.GET.get("page", "1")
    try:
        if pageSize != "all":
            pageSize = int(pageSize)
        else:
            pageSize = filtered_objects.count()
    except:
        pageSize = 10
    description = request.GET.get("desc", None)
    filtered_objects = Run.objects.all()
    if checkNotAllNull(
            (track, task, uploader_name,
             uploader_username, runtype,
             genre, feedback_type, map_min,
             map_max, p10_min, p10_max,
             p20_min, p20_max, date_min,
             date_max, name, description, organization,)):
        allNull = False
        try:
            date_min_c = getOrDefault(date_min, convertDate)
            date_max_c = getOrDefault(date_max, convertDate)
            if date_max_c is not None:
                date_max_c += datetime.timedelta(days=1) # Add one day
            p10_min_c = getOrDefault(p10_min, convertFloat)
            p10_max_c = getOrDefault(p10_max, convertFloat)
            p20_min_c = getOrDefault(p20_min, convertFloat)
            p20_max_c = getOrDefault(p20_max, convertFloat)
            map_min_c = getOrDefault(map_min, convertFloat)
            map_max_c = getOrDefault(map_max, convertFloat)
            if date_min_c is not None:
                filtered_objects = filtered_objects.filter(datetime__gte=date_min_c)
            if date_max_c is not None: # Since we added a day, we want it to be strictly less than it
                filtered_objects = filtered_objects.filter(datetime__lt=date_max_c)
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
            if task is not None:
                filtered_objects = filtered_objects.filter(task__title=task)
            if uploader_username is not None:
                filtered_objects = filtered_objects.filter(researcher__user__username=uploader_username)
            if uploader_name is not None:
                filtered_objects = filtered_objects.filter(researcher__display_name=uploader_name)
            if runtype is not None:
                filtered_objects = filtered_objects.filter(run_type=runtype)
            if feedback_type is not None:
                filtered_objects = filtered_objects.filter(feedback_type=feedback_type)
            if genre is not None:
                filtered_objects = filtered_objects.filter(task__track__genre__title=genre)
            if track is not None:
                filtered_objects = filtered_objects.filter(task__track__title=track)
            if name is not None:
                filtered_objects = filtered_objects.filter(name__contains=name)
            if description is not None:
                filtered_objects = filtered_objects.filter(description__contains=description)
            if organization is not None:
                filtered_objects = filtered_objects.filter(researcher__organization=organization)
            error = False
            paginator = Paginator(filtered_objects, pageSize)
            try:
                page = paginator.page(pageNo)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            context_dict["objects"] = page
        except:
            error = True
            context_dict["objects"] = None
    else:
        allNull = True
    # get complete URL querystring without rewriting it
    urlparams = request.GET.copy()
    if urlparams.has_key("page"):
        del (urlparams["page"])
    queryString = urlparams.urlencode()
    context_dict["querystring"] = queryString
    context_dict["error"] = error
    context_dict["allnull"] = allNull
    return render(request, "main/searchResults.html", context_dict)

def searchForm(request):
    context_dict = {}
    context_dict["tracks"] = Track.objects.all()
    context_dict["tasks"] = Task.objects.all()
    context_dict["genres"] = Genre.objects.all()
    context_dict["sizes"] = BrowseTaskForm.sizeChoices
    context_dict["run_type_choices"] = Run.Run_type_choices
    context_dict["feedback_type_choices"] = Run.Feedback_type_choices
    return render(request, "main/searchForm.html", context_dict)

def getOrgsJson(request):
    data = getJsonResponse(request, "organization", Researcher, "organization__contains")
    return HttpResponse(data, content_type='application/json')

def getUsrnameJson(request):
    data = getJsonResponse(request, "username", User, "username__contains")
    return HttpResponse(data, content_type='application/json')

def getNameJson(request):
    data = getJsonResponse(request, "display_name", Researcher, "display_name__contains")
    return HttpResponse(data, content_type='application/json')

def getRunNameJson(request):
    data = getJsonResponse(request, "name", Run, "name__contains")
    return HttpResponse(data, content_type='application/json')

def getTrackInfoJson(request):
    query = request.GET.get("track", None)
    if query is None or len(query.strip()) == 0:
        returnData = json.dumps([()])
    else:
        track = get_object_or_404(Track, id=query)
        returnData = []
        returnData.append(("Title", track.title,))
        returnData.append(("Description",track.description,))
        returnData.append(("URL", track.track_url,))
        returnData.append(("Genre",track.genre.title,))
        returnData = json.dumps(returnData)
    return HttpResponse(returnData, content_type="application/json")

def getTaskInfoJson(request):
    query = request.GET.get("task", None)
    if query is None or len(query.strip()) == 0:
        returnData = json.dumps([()])
    else:
        task = get_object_or_404(Task, id=query)
        returnData = []
        returnData.append(("Title",task.title,))
        returnData.append(("Description", task.description,))
        returnData.append(("URL",task.task_url,))
        returnData = json.dumps(returnData)
    return HttpResponse(returnData, content_type="application/json")

@staff_member_required
def manageTask(request):
    task_list = Task.objects.all()
    return render(request, "main/manageTask.html", {"list":task_list})

@staff_member_required
def manageTrack(request):
    track_list = Track.objects.all()
    return render(request, "main/manageTrack.html", {"list":track_list})

@staff_member_required
def manageGenre(request):
    genre_list = Genre.objects.all()
    return render(request, "main/manageGenre.html", {"list":genre_list})

@staff_member_required
def deleteTask(request, taskid):
    return viewhelper.deleteFormGeneric(request, "main/deleteConfirm.html", Task, taskid, "Task", reverse("manage_task"))

@staff_member_required
def deleteTrack(request, trackid):
    return viewhelper.deleteFormGeneric(request, "main/deleteConfirm.html", Track, trackid, "Track", reverse("manage_track"))

@staff_member_required
def deleteGenre(request, genreid):
    return viewhelper.deleteFormGeneric(request, "main/deleteConfirm.html", Genre, genreid, "Genre", reverse("manage_genre")
                                        , False)

def getTasksJson(request):
    query = request.GET.get("track", None)
    if query is None or len(query.strip()) == 0:
        returnData = json.dumps([()])
    else:
        tasks = Task.objects.filter(track__id=query).values_list("title", "description", "task_url")
        returnData = json.dumps(list(tasks))
    return HttpResponse(returnData, content_type="application/json")
