from django.db import models
from django.contrib.auth.models import User


'''
все объекты таблицы --- Post.objects.all() <--> select * from posts

один уникальный объект по условию --- Post.objects.get(id=1)

несколько объкетов по условию --- Post.objects.filter(title='title')

создание объектов - Post.objects.create(title='***', content='***')
'''

class Category(models.Model):
    name = models.CharField(max_length=24)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=24)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='posts')
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=156)
    content = models.CharField(max_length=1056)
    rate = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.title} - {self.content}'