from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class User(models.Model):
#   name = models.CharField(max_length=30)


class Post(models.Model):
  title = models.CharField(max_length= 50)
  content = models.TextField()
  user = models.ForeignKey(User)
  date = models.DateTimeField(auto_now_add=True)
  slug = models.SlugField(max_length=255, unique=True)

  def __unicode__(self):
        return self.title