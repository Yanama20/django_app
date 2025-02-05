from django.shortcuts import render, HttpResponse
import random

from posts.models import Post

def test_view(requset):
    return HttpResponse(f'Hello world! {random.randint(1, 100)}')

def html_view(request):
    return render(request, 'main.html')\
    
def post_list_view(request):
    posts = Post.objects.all()
    print(posts)
    for post in posts:
        print(post.title)
    return render(request, 'posts/post_list.html', context={'posts':posts})