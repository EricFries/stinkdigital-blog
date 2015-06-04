from django.shortcuts import render_to_response, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import RequestContext
from .models import Post, Comment, Tag, PostTags
from django.utils.text import slugify
from django import forms

#Login/Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import pdb

#Tag Views
# @login_required
def tag_new(request):
  return render(request, 'blog/new_tag.html')

# @login_required
def tag_create(request):
  tag = Tag(name = request.POST['name'], slug = slugify(request.POST['name']))
  tag.save()
  return redirect("/post/new")

#Post CRUD views
def posts_index(request):
  posts = Post.objects.all().order_by('-date')
  return render_to_response('blog/index.html', locals(), context_instance=RequestContext(request)
    )

# @login_required
def post_new(request):
  tags = Tag.objects.all()
  return render_to_response('blog/post_new.html', locals(), context_instance=RequestContext(request)
    )

# @login_required
def post_create(request):
  post = Post(title = request.POST['title'], content = request.POST['content'], slug = slugify(request.POST['title']))
  post.save()
  # user = request.user,

  tags_list = request.POST.getlist('tags')
  for tag_id in tags_list:
    tag = Tag.objects.get(pk=tag_id)
    pt = PostTags(post=post,tag=tag)
    pt.save()
  
  return redirect("/post/%s" % post.slug)

# class PostUpdateForm(forms.ModelForm):
#   class Meta:
#     model = Post
#     exclude = ('slug', 'user', 'date')

# class PostUpdateView(UpdateView):
#   model = Post
#   success_url = '/'
#   fields = ['title', 'content']
#   form_class = PostUpdateForm

def post_edit(request, slug):
  post = Post.objects.get(slug=slug)
  tags = Tag.objects.all()
  checked_tags = []
  for posttag in post.posttags_set.all():
    checked_tags.append(posttag.tag)

  return render_to_response('blog/post_edit.html', locals(), context_instance=RequestContext(request))

def post_edited(request, slug):
  post = Post.objects.get(slug=slug)
  post.title = request.POST['title']
  post.content = request.POST['content']
  post.save()

  #new tag ids to assign to post
  updated_tag_ids = request.POST.getlist('tags')

  #remove empty strings from list
  filter(None,updated_tag_ids)

  #check if currently assigned tags are in the updated_tag list, if not, delete the posttag object
  for pt in post.posttags_set.all():
    if pt.tag.id not in updated_tag_ids: 
      pt.delete()
    else:
      updated_tag_ids.remove(pt.tag)
  
  for tag_id in updated_tag_ids:
    tag = Tag.objects.get(pk=tag_id)
    pt = PostTags(post=post,tag=tag)
    pt.save()

  success_url = "/post/%s" % post.slug
  return redirect(success_url)

class PostDeleteView(DeleteView):
  model = Post
  success_url = '/'

class PostDetailView(DetailView):
  model = Post

  def get_context_data(self, **kwargs):
    context = super(PostDetailView, self).get_context_data(**kwargs)
    return context

#Comment Views
@login_required
def comment_delete(request):
  comment = Comment.objects.get(pk=request.POST['id'])
  post_slug = request.POST['post_slug']
  success_url = "/post/%s" % post_slug
  comment.delete()
  return redirect(success_url)

def comment_create(request):
  post = Post.objects.get(pk=request.POST['post_id'])
  comment = Comment(content = request.POST['content'], name = request.POST['name'], email = request.POST['email'], post = post)
  comment.save()
  return redirect("/post/%s" % post.slug)

#Session Views
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
    messages.error(request, 'Failed to login. Please try again.')
    return redirect('/login')
  