from django.db import models

# Create your models here.
class User(models.Model):
  name = models.CharField(max_length=30)


class Post(models.Model):
  title = models.CharField(max_length= 50)
  content = models.TextField()
  user = models.ForeignKey(User)