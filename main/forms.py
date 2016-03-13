from django import forms
from main.models import Task, Track, Run, Researcher
from captcha.fields import CaptchaField
from parsley.decorators import parsleyfy
from django.contrib.auth.models import User

@parsleyfy
class RunForm(forms.ModelForm):
    task = forms.ChoiceField(choices=Task.objects.all())
    captcha = CaptchaField(required=True, label="Verify you are not a robot")
    class Meta:
        model = Run
        fields = ('name', 'description', 'result_file', 'run_type', 'query_type', 'feedback_type',)


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

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
