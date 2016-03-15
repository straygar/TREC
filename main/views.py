from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required

from main.forms import RunForm
from main.models import Task
from main.forms import RunForm, UserForm, UserProfileForm

from django.contrib.auth.models import User
from .models import Researcher
from django.template import RequestContext

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'main/home.html')

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

def register(request):
    # Request the context.
    context = RequestContext(request)
    context_dict = {}
    # Boolean telling us whether registration was successful or not.
    # Initially False; presume it was a failure until proven otherwise!
    registered = False

    # If HTTP POST, we wish to process form data and create an account.
    if request.method == 'POST':
        # Grab raw form data - making use of both FormModels.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Two valid forms?
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data. That one is easy.
            user = user_form.save()

            # Now a user account exists, we hash the password with the set_password() method.
            # Then we can update the account with .save().
            user.set_password(user.password)
            user.save()

            # Now we can sort out the UserProfile instance.
            # We'll be setting values for the instance ourselves, so commit=False prevents Django from saving the instance automatically.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Profile picture supplied? If so, we put it in the new UserProfile.
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            # Now we save the model instance!
            profile.save()

            # We can say registration was successful.
            registered = True

        # Invalid form(s) - just print errors to the terminal.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render the two ModelForms to allow a user to input their data.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict['user_form'] = user_form
    context_dict['profile_form']= profile_form
    context_dict['registered'] = registered

    # Render and return!
    return render_to_response(
        'main/register.html',
        context_dict,
        context)


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

            # We'll be setting values for the instance ourselves, so commit=False prevents Django from saving the instance automatically.
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
    # As we can assume the user is logged in, we can just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/main/')


@login_required
def profile(request):
    context = RequestContext(request)
    context_dict={}

    u = User.objects.get(username=request.user)
    try:
        up = Researcher.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('main/profile.html', context_dict, context)


def index(request):

    response=render(request,"main/index.html")
    return response

def about(request):
    return render(request,'main/about.html')