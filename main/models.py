from django.db import models
from django.contrib.auth.models import User

class Researcher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True
    )
    profile_picture = models.CharField(max_length=64, unique=True)
    website = models.CharField(max_length=64, unique=False)
    display_name = models.CharField(max_length=128, unique=False)
    organization = models.CharField(max_length=128, unique=False)

class Track(models.Model):
    # Genre enums
    GE_News = "NE"
    GE_Web = "WE"
    GE_Blog = "BL"
    GE_Medical = "ME"
    GE_Legal = "LE"
    Genre_choices = (
        (GE_News, "News"),
        (GE_Web, "Web"),
        (GE_Blog, "Blog"),
        (GE_Medical, "Medical"),
        (GE_Legal, "Legal"),
    )
    title = models.CharField(max_length = 64, unique=True)
    track_url = models.URLField(max_length=200)
    description = models.CharField(max_length=400)
    genre = models.CharField(max_length=2, choices = Genre_choices)

class Task(models.Model):
    def __unicode__(self):
        return u'{0}'.format(self.title)

    track = models.OneToOneField(
        Track,
        on_delete = models.CASCADE,
        primary_key = True
    )
    title = models.CharField(max_length = 64, unique=True)
    task_url = models.URLField(max_length=200)
    description = models.CharField(max_length = 400)
    year = models.IntegerField()
    judgement_file = models.CharField(max_length=40)

class Run(models.Model):
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
    description = models.CharField(max_length=400, unique=False)
    result_file = models.FileField(upload_to='trec_upload/%Y/%m/%d/')
    run_type = models.CharField(max_length=2, choices=Run_type_choices)
    query_type = models.CharField(max_length=2, choices=Query_type_choices)
    feedback_type = models.CharField(max_length=2, choices=Feedback_type_choices)
    map = models.DecimalField(max_digits=200, decimal_places = 30)
    p10 = models.DecimalField(max_digits=200, decimal_places = 30)
    p20 = models.DecimalField(max_digits=200, decimal_places = 30)