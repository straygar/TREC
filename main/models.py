from django.db import models
from django.contrib.auth.models import User

class Researcher(models.Model):
    profile_picture = models.CharField(max_length=64, unique=True)
    website = models.CharField(max_length=64, unique=False)
    display_name = models.CharField(max_length=128, unique=False)
    organization = models.CharField(max_length=128, unique=False)


