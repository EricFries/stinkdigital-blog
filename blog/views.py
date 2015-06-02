# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext
from .models import Post, User
from django.utils import timezone
import pdb

def index(request):
  posts = Post.objects.all()
  return render_to_response('blog/index.html',
            locals(), context_instance=RequestContext(request)
    )

def new(request):
  return render(request, 'blog/new.html')

def create(request):
  user, created = User.objects.get_or_create(name="Eric")

  post = Post(title = request.POST['title'], content = request.POST['content'])
  post.user = user
  post.save()
  return redirect('/')