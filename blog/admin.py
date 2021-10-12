from django.contrib import admin
from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ('id', 'date_published', 'title', 'author',)
    list_filter = ['date_published']


admin.site.register(Blog, BlogAdmin)
