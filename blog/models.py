from django.db import models

# Create your models here.
class Author(models.Model):
  name = models.CharField(max_length=30)

class Post(models.Model):
  author = models.ForeignKey(Author)
  title = models.CharField(max_length= 50)
  content = models.TextField() 