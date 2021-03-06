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
    sizeChoices = (
        ("10", "10 items"),
        ("25", "25 items"),
        ("40", "40 items"),
        ("all", "Get all items"),
    )
    size = forms.ChoiceField(choices=sizeChoices, label="Results per page")
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
        ("AL", "All three scores - get best (or worst) runs"),
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
    username = forms.CharField(help_text="Username", widget=forms.TextInput(attrs={'placeholder': 'Username *'}), 
		error_messages={'required':"Please enter a username"})
    email = forms.CharField(help_text="E-mail", widget=forms.TextInput(attrs={'placeholder': 'e-Mail *'}),
		error_messages={'required':"Please enter an e-mail address",'invalid':"Enter a valid e-mail address (e.g. 'user@gmail.com')"})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password *'}), help_text="Password",
		error_messages={'required':"Please enter a password"})

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
		

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Website", required=False, widget=forms.TextInput(attrs={'placeholder': 'Website'}),
		error_messages={'invalid':"Please enter a valid website (e.g. 'http://www.google.com/)'"})
    profile_picture = forms.ImageField(help_text="Profile picture", required=False)
    display_name = forms.CharField(help_text="Name",required=True, widget=forms.TextInput(attrs={'placeholder': 'Name *'}),
		error_messages={'required':"Please enter a name"})
    organization = forms.CharField(help_text="Organisation",required=False, widget=forms.TextInput(attrs={'placeholder': 'Organisation'}))

    class Meta:
        model = Researcher
        fields = ('display_name','website','organization', 'profile_picture')

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
