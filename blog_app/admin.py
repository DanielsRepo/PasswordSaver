from django.contrib import admin
from blog_app.models import Post, Theme

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('pk', )
    list_display = ('title', 'text', 'theme', 'created_date', 'published_date')
    list_display_links = ('title', 'text')
    search_fields = ('title', 'text')

admin.site.register(Post, PostAdmin) # Чтобы приложение появилось в списке административного сайта
admin.site.register(Theme) # Чтобы приложение появилось в списке административного сайта

