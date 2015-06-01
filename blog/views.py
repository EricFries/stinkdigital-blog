# Create your views here.
from django.shortcuts import get_object_or_404, render
from .models import Author, Post
from django.utils import timezone
from IPython import embed

def index(request):
  return render(request, 'blog/index.html')

def new(request):
  return render(request, 'blog/new.html')

def create(request):
  return render(request, 'blog/index.html')