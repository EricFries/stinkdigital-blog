# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from .models import Post
from django.utils import timezone
import pdb

# def index(request):
#   # pdb.set_trace();
#   posts = Post.objects.all()
#   return render(request, 'blog/index.html')

def index(request):
  posts = Post.objects.all()
  return render_to_response('blog/index.html',
            locals(), context_instance=RequestContext(request)
    )

def new(request):
  return render(request, 'blog/new.html')

def create(request):
  post = Post(title = request.POST['title'], content = request.POST['content'])
  post.save()
  return render(request, 'blog/index.html')