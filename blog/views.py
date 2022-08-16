from django.shortcuts import render
from .models import Blogpost
# Create your views here.
from django.http import HttpResponse


def index(request):
    mypost = Blogpost.objects.all()
    print(mypost)
    return render (request, 'blog/index.html' , {'mypost':mypost})

def blogpost(request , slug):
    post = Blogpost.objects.filter(slug=slug)[0]
    print(post)
    return render (request, 'blog/blogpost.html', {'post':post})