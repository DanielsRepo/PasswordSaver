from django.conf import settings
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
    title = models.CharField(max_length = 200, null=True)

    # title = models.CharField(max_length = 200, validators = [validators.MinLengthValidator(5)],
    # error_message={'min_length' : 'ERROR!'})

    text = models.TextField(null=True, verbose_name='Описание')
    theme = models.ForeignKey('Theme', null=True, on_delete=models.CASCADE, verbose_name='Тема', related_name='entries')
    # null = True - необязаьльеоне поле

    created_date = models.DateTimeField(null=True, default=timezone.now, verbose_name='Создано')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='Опубликовано')

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
        return reverse('post_detail', kwargs={'pk': self.pk})

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
    theme_name = models.CharField(null=True, max_length=200, db_index=True, verbose_name='Тема')

    def __str__(self):
        return self.theme_name

    def get_absolute_url(self):
        return f'/theme/{self.pk}'

    class Meta:
        verbose_name_plural = 'Темы'
        verbose_name = 'Тема'


