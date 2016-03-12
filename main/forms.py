from django import forms
from main.models import Task, Track, Run
from captcha.fields import CaptchaField
from parsley.decorators import parsleyfy

@parsleyfy
class RunForm(forms.ModelForm):
    task = forms.ChoiceField(choices=Task.objects.all())
    captcha = CaptchaField(required=True, label="Verify you are not a robot")
    class Meta:
        model = Run
        fields = ('name', 'description', 'result_file', 'run_type', 'query_type', 'feedback_type',)
