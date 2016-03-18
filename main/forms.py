from django import forms
from main.models import Task, Track, Run, Researcher, RunFile, Genre
from captcha.fields import CaptchaField
from parsley.decorators import parsleyfy
from django.contrib.auth.models import User

class BrowseForm(forms.ModelForm):
    track = forms.ModelChoiceField(queryset=Track.objects.all())
    task = forms.ModelChoiceField(queryset=Task.objects.all())
    class Meta:
        model = Track
        fields = ('track', 'task')

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

    website = forms.URLField(help_text="Please enter your website.", required=False)
    profile_picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
    display_name = forms.CharField(help_text="Please enter your name",required=False)
    organization = forms.CharField(help_text="Please enter the name of your organization",required=False)

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