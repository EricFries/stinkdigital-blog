# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.views.generic.detail import DetailView
from django.template import RequestContext
from .models import Post

from django.utils.text import slugify

from django.contrib.auth import authenticate, login, logout

#debugger
# import sys
# for attr in ('stdin', 'stdout', 'stderr'):
#     setattr(sys, attr, getattr(sys, '__%s__' % attr))
# import pdb

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
  # user, created = User.objects.
  post = Post(title = request.POST['title'], content = request.POST['content'], slug = slugify(request.POST['title']))
  post.save()
  return redirect("/post/%s" % post.slug)

def login_view(request):
  return render(request, 'blog/login.html')

def logout_view(request):
  logout(request)
  return redirect('/')

def auth_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    login(request, user)
    return redirect('/')
  else:
    #add failed to login error
     return redirect('/login')
  