from django.conf import settings
from django.core import validators
from django.db import models
from django.utils import timezone
from django.urls import reverse

class PostManager(models.Manager):
    def by_theme(self, pk):
        return self.filter(published_date__lte=timezone.now(), theme = pk).order_by('-published_date')

    def published(self):
        return self.filter(published_date__lte=timezone.now()).order_by('-published_date')

    def drafts(self):
        return self.filter(published_date__isnull=True).order_by('-created_date')
    
    def by_user(self, user):
        return self.published().filter(author=user)
        # return self.filter(published_date__lte=timezone.now(), author=user).order_by('-published_date')

class Post(models.Model): # вторичная ведомая
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)
    title = models.CharField(max_length = 200, null = True)
    # title = models.CharField(max_length = 200, validators = [validators.MinLengthValidator(5)], error_message={'min_length' : 'ERROR!'})

    text = models.TextField(null = True, verbose_name='Описание')
    theme = models.ForeignKey('Theme', null = True, on_delete = models.CASCADE, verbose_name = 'Тема', related_name='entries')
    # null = True - необязаьльеоне поле

    created_date = models.DateTimeField(null = True, default = timezone.now, verbose_name='Создано')
    published_date = models.DateTimeField(blank = True, null = True, verbose_name='Опубликовано')

    objects = PostManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        print(f'{self} published {self.author}')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(f'{self} saved')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        print(f'{self} deleted')

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})

    # функциональное поле
    # def title_by_len(self):
    #     print(self)
    #     if len(self.title) > 5:
    #         return self.title

    # title_by_len.short_description = 'TITLE'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

class Theme(models.Model): # первичная ведущая
    theme_name = models.CharField(null = True, max_length = 200, db_index = True, verbose_name = 'Тема')

    def __str__(self):
        return self.theme_name

    def get_absolute_url(self):
        return f'/theme/{self.pk}'

    class Meta:
        verbose_name_plural = 'Темы'
        verbose_name = 'Тема'

# c:/Django/site/Scripts/activate.ps1

# createsuperuser

# from blog_app.models import Post, Theme

# from django.contrib.auth.models import User
#  u = User.objects.get(username='dancher')

# p = Post(author=u, title='AAAA', text='AAAA')
# p.save()
# p.save(update_fiels=['title'])


# p = Post.objects.get(pk = 29)
# p.publish()

# t = Theme.objects.create(pk = 2, theme_name = 'Тема 2')
# Theme.objects.filter(pk=1).delete()
# t = Theme.objects.get_or_create(theme_name='THEME')
# p = Post.objects.update_or_create(title = 'AAAA', defaults={'text':'AAAAAAAAAAAAAAAA'})
# for i in Post.objects.all():
# ...     i.theme = Theme.objects.get(pk=random.randint(2,4))
# ...     i.save()

# p = PostForm({'title':'as','text':'assss','theme':'Тема 2'})

# t = Theme.objects.get(theme_name="Тема 2")
# for i in t.entries.all():
# ...     print(i.title)

# post_set = related_name

# >>> t.post_set.earliest('published_date')
# <Post: wegewg>
# >>> t.post_set.earliest('-published_date')
# <Post: er5yhewrs>
# >>> t.post_set.latest('-published_date')
# <Post: wegewg>
# >>> Post.objects.filter(theme = t).exists()
# True
# >>> Post.objects.filter(theme = t).count()
# 6

# get_next_by_<имя поля> 1 get_previous_by_<имя поля>([<условия поиска>]) 
# exclude - противоположность filter

# >>> for i in Post.objects.filter(theme__theme_name = 'Тема 2'):
# ...     print(i.title)

# for i in Post.objects.filter(Q(theme__theme_name='Тема 2') | Q(theme__theme_name='Тема 3')):
# ...     print(i.title)

# distinct - уникальные записи

# result = Bb.objects.aggregate(Min('price'), Max('price'))
# >>> result['price_min'], result['price_max'] 
# result = Bb.objects.aggregate(diff=Max('price')-Min('price'))
# >>> result['diff'] 

# for i in Theme.objects.annotate(cnt = Count('post')):
# ...     print(i.theme_name, " : ", i.cnt)

# вычисляемое поле
# >>> from django.dЬ.models import ExpressionWrapper, IntegerField
# >>> for Ь in Bb.objects.annotate(
# half_price=ExpressionWrapper(F('price')/2,IntegerField())):
# print(b.title, b.half_price) 

# aggregate по всем записям модели
# annotate по группам

# sq = Subquery(Post.objects.filter(theme = OuterRef('pk')).order_by('-published_date').values('published_date')[:1])
# >>> for i in Theme.objects.annotate(last_post_date = sq):
# ...     print(i.theme_name, i.last_post_date)

# >>> from django.dЬ.models import Exists
# >>> subquery = Exists(Bb.objects.filter(rubric=OuterRef('pk'),
# price~gt=l00000))
# >>> for r in RuЬric.objects.annotate(is_expensive=suЬquery) .filter(
# is_expensive=True): print(r.name) 


# union intersection difference
# >>> p1 = Post.objects.filter(theme = Theme.objects.get(theme_name = 'Тема 3'))
# >>> p2 = Post.objects.filter(theme = Theme.objects.get(theme_name = 'Тема 2'))
# >>> for i in p1.union(p2):
# ...     print(i.title)

# >>> from django.db.models import F
# >>> Post.objects.values('title', themeName = F('theme')) возвращ queryset
# >>> Post.objects.values_list('title', 'theme') возвращ кортежи
# Post.objects.values_list('title', flat=True) для одного поля

# >>> Post.objects.dates('published_date', 'month') с уникал знач даты месяца
# datetimes тоже но плюс время 

# >>> Post.objects.in_bulk([1,2,3,4,5], field_name='pk')

# PostManager
# objects = PostManager()