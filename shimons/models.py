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
    date_created = models.DateTimeField(null=True, auto_now=True)
    date_modified = models.DateTimeField(null=True)
    status = models.SmallIntegerField(default=1, blank=True, null=False)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return self.title


class DashboardPost(models.Model):
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


class RequestModel(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128,null=False, default="req_" + str(id))
    date = models.DateField(null=False)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Algorithm(models.Model):
    request = models.OneToOneField(RequestModel, on_delete=models.CASCADE)
    jar_path = models.CharField(null=False, max_length=256)
    main_jarFile = models.CharField(null=False, max_length=128)
    src_path = models.CharField(null=True, max_length=256)

    def __str__(self):
        return "algorihm for " + str(self.request)


class Patterns(models.Model):
    pattern_path = models.CharField(null=False, max_length=255)
    request = models.OneToOneField(RequestModel, on_delete=models.CASCADE)

    def __str__(self):
        return "Pattern for " + str(self.request)
