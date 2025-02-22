from django.shortcuts import render, HttpResponse, redirect
import random

from posts.models import Post

from posts.forms import PostCreateForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def test_view(requset):
    return HttpResponse(f'Hello world! {random.randint(1, 100)}')

def html_view(request):
    return render(request, 'main.html')\
    

@login_required(login_url='/login/')
def post_list_view(request):
    form = SearchForm()
    query_params = request.GET
    limit = 3
    if request.method == 'GET':
        posts = Post.objects.all()
        search = query_params.get('search')
        category_id = query_params.get('category')
        tags = query_params.getlist('tags')
        ordering = query_params.get('ordering')
        page = int(query_params.get('page')) if query_params.get('page') else 1
        if search:
            posts = posts.filter(
                Q(title__contains=search) | Q(content__icontains=search)
            )

        if category_id:
            posts = posts.filter(category_id=category_id)

        if tags:
            tags = [int(tag) for tag in tags]
            posts = posts.filter(tags__id__in=tags) 
        
        if ordering:
            posts = posts.order_by(ordering)

        max_pages = posts.count() / limit
        if round(max_pages) < max_pages:
            max_pages = round(max_pages) + 1
        else:
            max_pages = round(max_pages)

        start = (page - 1)  * limit
        end = page * limit
        posts = posts[start:end]
        context_data = {'posts':posts, 'form':form, 'max_pages':range(1, max_pages + 1)}

        return render(request, 'posts/post_list.html', context=context_data)



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
        
