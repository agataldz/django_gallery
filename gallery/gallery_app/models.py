from django.contrib.auth.models import User
from django.db import models


class Photo(models.Model):
    photo = models.ImageField(upload_to='photos')
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    username = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    photo = models.ForeignKey(Photo, null=True, blank=True)
    content = models.TextField(max_length=1024)
    username = models.ForeignKey(User, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
