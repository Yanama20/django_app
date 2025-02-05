from django.db import models

'''
все объекты таблицы --- Post.objects.all() <--> select * from posts

один уникальный объект по условию --- Post.objects.get(id=1)

несколько объкетов по условию --- Post.objects.filter(title='title....')

'''

class Post(models.Model):
    title = models.CharField(max_length=156)
    content = models.CharField(max_length=1056)
    rate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.content}'