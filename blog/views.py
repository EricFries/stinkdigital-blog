# Create your views here.
from django.shortcuts import get_object_or_404, render
from .models import Author, Post
from django.utils import timezone
import pdb

def index(request):
  posts = Post.objects.all()
  return render(request, 'blog/index.html')

def new(request):
  return render(request, 'blog/new.html')

def create(request):
  # pdb.set_trace();
  author = Author(name="Eric")
  author.save()
  post = Post(title = request.POST['title'], content = request.POST['content'])
  post.author = author
  post.save()
  return render(request, 'blog/index.html')