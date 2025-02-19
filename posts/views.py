from django.shortcuts import render, HttpResponse, redirect
import random

from posts.models import Post

from posts.forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def test_view(requset):
    return HttpResponse(f'Hello world! {random.randint(1, 100)}')

def html_view(request):
    return render(request, 'main.html')\
    

@login_required(login_url='/login/')
def post_list_view(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        return render(request, 'posts/post_list.html', context={'posts':posts})

@login_required(login_url='/login/')
def post_detail_view(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(id = post_id)
        return render(request, 'posts/post_detail.html', context={'post':post})


@login_required(login_url='/login/')
def post_create_view(request):
    if request.method == 'GET':
        form = PostCreateForm()
        return render(request, 'posts/post_create.html', context={"form": form})
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'posts/post_create.html', context={"form": form})
        elif form.is_valid():
            image = form.cleaned_data.get("image")
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            post = Post.objects.create(image=image, title=title, content=content)
        # data = request.POST
        # image = request.FILES.get("image")
        # title = data.get("title")
        # content = data.get("content")   
        
        if post:
            return redirect('/posts/')
        else:
            return HttpResponse('Пост не был создан.')
        
