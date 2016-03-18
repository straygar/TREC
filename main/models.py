from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from registration.signals import user_registered
from django.utils import timezone

def upload_profile(instance, filename):
    return "profile/%s/%s" % (instance.user.username, filename)

class Researcher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True
    )
    profile_picture = models.ImageField(upload_to=upload_profile, blank=False)
    website = models.CharField(max_length=64, unique=False, blank=True)
    display_name = models.CharField(max_length=128, unique=False)
    organization = models.CharField(max_length=128, unique=False, blank=True)

class Genre(models.Model):
    def __unicode__(self):
        return u'{0}'.format(self.title)
    title = models.CharField(max_length=64, unique=True)

class Track(models.Model):
    def __unicode__(self):
        return u'{0}'.format(self.title)
    title = models.CharField(max_length = 64, unique=True)
    track_url = models.URLField(max_length=200)
    description = models.CharField(max_length=400)
    genre = models.ForeignKey(
        Genre, on_delete=models.PROTECT,
    )

class Task(models.Model):
    def __unicode__(self):
        return u'{0}'.format(self.title)

    track = models.ForeignKey(
        Track,
        on_delete = models.CASCADE
    )
    title = models.CharField(max_length = 64, unique=True)
    task_url = models.URLField(max_length=200)
    description = models.CharField(max_length = 400)
    year = models.PositiveSmallIntegerField()
    judgement_file = models.FileField(upload_to="trec_tracks/%Y/%m/")

class RunFile(models.Model):
    result_file = models.FileField(upload_to="trec_upload/%Y/%m/%d/")

class Run(models.Model):
    def save(self, *args, **kwargs):
        self.datetime = timezone.now()
        super(Run, self).save(*args, **kwargs)
    # Run_type enums
    RT_Automatic = "AU"
    RT_Manual = "MA"
    Run_type_choices = (
        (RT_Automatic, "Automatic"),
        (RT_Manual, "Manual"),
    )

    # Query_type enums
    QT_Title_only = "TO"
    QT_Title_Desc = "TD"
    QT_Desc_only = "DO"
    QT_All_fields = "AF"
    QT_Other = "UF" # Unknown fields
    Query_type_choices = (
        (QT_Title_only, "Title only"),
        (QT_Title_Desc, "Title + description"),
        (QT_Desc_only, "Description"),
        (QT_All_fields, "All"),
        (QT_Other, "Other"),
    )

    #Feedback_type enums
    FT_None = "NF"
    FT_Pseudo = "PF"
    FT_Relevance = "RF"
    FT_Other = "OF"
    Feedback_type_choices = (
        (FT_None, "None"),
        (FT_Pseudo, "Pseudo"),
        (FT_Relevance, "Relevance"),
        (FT_Other, "Other"),
    )

    researcher = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=False)
    datetime = models.DateTimeField()
    result_file = models.OneToOneField(
        RunFile,
        on_delete = models.CASCADE,
    )
    description = models.CharField(max_length=400, unique=False)
    run_type = models.CharField(max_length=2, choices=Run_type_choices)
    query_type = models.CharField(max_length=2, choices=Query_type_choices)
    feedback_type = models.CharField(max_length=2, choices=Feedback_type_choices)
    map = models.DecimalField(max_digits=15, decimal_places=12)
    p10 = models.DecimalField(max_digits=15, decimal_places=12)
    p20 = models.DecimalField(max_digits=15, decimal_places=12)