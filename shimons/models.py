from django.db import models
from custom_user.models import AbstractEmailUser


class UserProfile(AbstractEmailUser):
    education = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    university = models.CharField(max_length=128, null=True)
    field = models.ForeignKey('Field', on_delete=models.SET_NULL, null=True)
    def __unicode__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return self.email


class Post(models.Model):
    title = models.CharField(max_length=128, unique=True)
    subtitle = models.CharField(max_length=256)
    content = models.TextField()
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    status = models.SmallIntegerField(default=1, blank=True, null=False)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return self.title


class DashboardPosts(models.Model):
    title = models.CharField(max_length=128, unique=True)
    subtitle = models.CharField(max_length=256)
    content = models.TextField()
    date_created = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    status = models.SmallIntegerField(default=1, blank=True, null=False)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return self.title


class Field(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return self.name
