from django.shortcuts import render, HttpResponse, redirect
import random
from posts.models import Post
from posts.forms import PostCreateForm, PostUpdateForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView


def test_view(request):
    return HttpResponse(f'Hello world! {random.randint(1, 100)}')

def html_view(request):
    if request.method == 'GET':
        return render(request, 'main.html')
    else:
        return None

class TestView(View):
    def get(self, request):
        return HttpResponse(f'Hello world! {random.randint(1, 100)}')    

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

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    def get_queryset(self):
        query_params = self.request.GET
        queryset = Post.objects.all()

        category_id = query_params.get('category')
        tags = query_params.getlist('tags')
        ordering = query_params.get('ordering')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if tags:
            tags = [int(tag) for tag in tags] 
            queryset = queryset.filter(tags__id__in=tags)

        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context

@login_required(login_url='/login/')
def post_detail_view(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(id = post_id)
        return render(request, 'posts/post_detail.html', context={'post':post})
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


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
    
class PostCreateView(CreateView):
    model = Post
    success_url = '/posts/'
    template_name = 'posts/post_create.html'
    form_class = PostUpdateForm

        
@login_required(login_url='/login/')
def post_update_view(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post не найден.")
    if request.method == "GET":
        form = PostUpdateForm(instance=post)
        return render(request, 'posts/post_update.html', context={'form': form})
    if request.method == "POST":
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if not form.is_valid():
            return render(request, 'posts/post_update.html', context={'form': form})
        elif form.is_valid():
            form.save()
            return redirect('/profile/')
        else:
            return HttpResponse('Post не был обновлён')


class PostUpdateView(UpdateView):
    model = Post
    success_url = '/profile/'
    template_name = 'posts/post_update.html'
    form_class = PostUpdateForm
    pk_url_kwarg = 'post_id'

