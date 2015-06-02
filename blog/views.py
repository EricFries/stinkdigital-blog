# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.views.generic.detail import DetailView
from django.template import RequestContext
from .models import Post, User
from django.utils import timezone
from django.utils.text import slugify
import pdb

class PostDetailView(DetailView):
  model = Post

  def get_context_data(self, **kwargs):
    context = super(PostDetailView, self).get_context_data(**kwargs)
    return context

def index(request):
  #Orders posts by date in descending order
  posts = Post.objects.all().order_by('-date')
  return render_to_response('blog/index.html', locals(), context_instance=RequestContext(request)
    )

def new(request):
  return render(request, 'blog/new.html')

def create(request):
  #Assigns the True/False return value to 'created' so user is always an instance of User.
  user, created = User.objects.get_or_create(name="Eric")
  post = Post(title = request.POST['title'], content = request.POST['content'], slug = slugify(request.POST['title']))
  post.user = user
  post.save()
  return redirect("/post/%s" % post.slug)