from django.http import HttpResponse
import json
from django.shortcuts import render_to_response, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import RequestContext
from .models import Post, Comment, Tag, PostTags
from django.utils.text import slugify
from django import forms

#for comment create
from django.template.loader import render_to_string

#Login/Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#Post CRUD views
def posts_index(request):
  posts = Post.objects.all().order_by('-date')
  return render_to_response('blog/index.html', locals(), context_instance=RequestContext(request)
    )

@login_required
def post_new(request):
  tags = Tag.objects.all()
  return render_to_response('blog/post_new.html', locals(), context_instance=RequestContext(request)
    )

@login_required
def post_create(request):
  post = Post(title = request.POST['title'], content = request.POST['content'], user = request.user, slug = slugify(request.POST['title']))
  post.save()

  tags_list = request.POST.getlist('tags')
  for tag_id in tags_list:
    tag = Tag.objects.get(pk=tag_id)
    pt = PostTags(post=post,tag=tag)
    pt.save()
  
  return redirect("/post/%s" % post.slug)

@login_required
def post_edit(request, slug):
  post = Post.objects.get(slug=slug)
  tags = Tag.objects.all()
  checked_tags = []
  for posttag in post.posttags_set.all():
    checked_tags.append(posttag.tag)

  return render_to_response('blog/post_edit.html', locals(), context_instance=RequestContext(request))

@login_required
def post_edited(request, slug):
  post = Post.objects.get(slug=slug)
  post.title = request.POST['title']
  post.content = request.POST['content']
  post.save()

  #New tag ids to assign to edited post
  updated_tag_ids = request.POST.getlist('tags')

  #Check if currently assigned tags are in the updated_tag list, if not, delete the posttag object.  If they are, remove them from the list of tags to add to the post.
  for pt in post.posttags_set.all():
    if pt.tag.id not in updated_tag_ids: 
      pt.delete()
    else:
      updated_tag_ids.remove(pt.tag)
  
  #For tags remaining, create new posttag objects
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
  post = comment.post
  
  response_data = {}
  response_data['id'] = comment.id
  comment.delete()
  post.save()
  count = post.comment_set.all().count()
  response_data['count'] = count
  
  return HttpResponse(json.dumps(response_data), content_type="application/json")

def comment_create(request):
  post = Post.objects.get(pk=request.POST['post_id'])
  comment = Comment(content = request.POST['content'], name = request.POST['name'], email = request.POST['email'], post = post)
  comment.save()

  if request.is_ajax():
    html = render_to_string('blog/new_comment.html', {'comment': comment})
    return HttpResponse(html)
  # response_data = {}
  # response_data['name'] = comment.name
  # response_data['email'] = comment.email
  # response_data['content'] = comment.content
  # response_data['id'] = comment.id
  # response_data['date'] = comment.date.strftime("%B %d, %Y")
  # # response_data['count'] = post.comment_set.all().count()

  # return HttpResponse(json.dumps(response_data), content_type="application/json")

#Tag Views
@login_required
def tag_new(request):
  return render(request, 'blog/new_tag.html')

@login_required
def tag_create(request):
  tag = Tag(name = request.POST['name'], slug = slugify(request.POST['name']))
  tag.save()
  return redirect("/post/new")

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
  