from django import forms
from main.models import Task, Track, Run, Researcher, RunFile, Genre
from captcha.fields import CaptchaField
from parsley.decorators import parsleyfy
from django.contrib.auth.models import User


class BrowseForm(forms.ModelForm):
    task = forms.ModelChoiceField(queryset=Task.objects.all())

class BrowseTrackForm(forms.ModelForm):
    track = forms.ModelChoiceField(queryset=Track.objects.all())
    class Meta:
        model = Track
        fields = ('track',)

class BrowseTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        thisTask = kwargs.pop("track", None)
        super(BrowseTaskForm, self).__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.objects.filter(track=thisTask)
    task = forms.ModelChoiceField(queryset=Track.objects.all())

    class Meta:
        model = Task
        fields = ('task',)

class BrowseTaskSortForm(forms.Form):
    sortChoices = (
        ("", "Do not sort"),
        ("DA", "Date uploaded"),
        ("P1", "P10 score"),
        ("P2", "P20 score"),
        ("MA", "Map score"),
        ("FT", "Feedback type"),
        ("RT", "Run type"),
        ("QT", "Query type"),
        ("UO", "Uploader organization"),
        ("UU", "Uploader username"),
        ("UN", "Uploader name"),
        ("TL", "Title"),
    )
    sortOrder = (
        ("DE", "Descending"),
        ("AS", "Ascending"),
    )
    sortOn = forms.ChoiceField(choices=sortChoices, label="Sort by...")
    sortOrd = forms.ChoiceField(choices=sortOrder, label="Sort order")

@parsleyfy
class RunForm(forms.ModelForm):
    task = forms.ModelChoiceField(queryset=Task.objects.all())
    captcha = CaptchaField(required=True, label="Verify you are not a robot")
    class Meta:
        model = Run
        fields = ('name', 'description', 'run_type', 'query_type', 'feedback_type',)

class RunFileForm(forms.ModelForm):
    result_file = forms.FileField(label="Select run file")
    class Meta:
        model = RunFile
        fields = ('result_file',)

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Username")
    email = forms.CharField(help_text="E-mail")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
		

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Website", required=False)
    profile_picture = forms.ImageField(help_text="Profile picture", required=False)
    display_name = forms.CharField(help_text="Name",required=False)
    organization = forms.CharField(help_text="Organization",required=False)

    class Meta:
        model = Researcher
        fields = ('website', 'profile_picture','display_name','organization')

class TaskForm(forms.ModelForm):
    track = forms.ModelChoiceField(queryset=Track.objects.all())
    judgement_file = forms.FileField(label="Select a qrels file")

    class Meta:
        model = Task
        fields = ('track', 'title', 'description', 'task_url', 'year', 'judgement_file',)

class TrackForm(forms.ModelForm):

    class Meta:
        model = Track
        fields = ('title', 'track_url', 'description', 'genre',)

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('title',)

class ReturnUrlForm(forms.Form):
    url = forms.URLField(max_length=300, widget=forms.HiddenInput(), required=False)
