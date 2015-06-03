from django.shortcuts import render_to_response, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import RequestContext
from .models import Post, Comment

from django.utils.text import slugify

#Login/Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django import forms

# debugger
import sys
for attr in ('stdin', 'stdout', 'stderr'):
    setattr(sys, attr, getattr(sys, '__%s__' % attr))
import pdb

def comment_create(request):
  post = Post.objects.get(pk=request.POST['post_id'])
  comment = Comment(content = request.POST['content'], name = request.POST['name'], email = request.POST['email'], post = post)
  comment.save()
  post.save()
  return redirect("/post/%s" % post.slug)

class PostUpdateForm(forms.ModelForm):
  class Meta:
    model = Post
    exclude = ('slug', 'user', 'date')

class PostUpdateView(UpdateView):
  model = Post
  success_url = '/'
  fields = ['title', 'content']
  form_class = PostUpdateForm

class PostDeleteView(DeleteView):
  model = Post
  success_url = '/'

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

# @login_required
def new(request):
  return render(request, 'blog/new.html')

# @login_required
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
  