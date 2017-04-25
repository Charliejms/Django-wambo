# -*- coding:utf8 -*-
from django.contrib import admin

# Register your models here.
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'updated']
    list_display_links = ['title']
    list_filter = ['updated', 'timestamp']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',), }
    date_hierarchy = 'publish'

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_at']
    list_filter = ['title']
    search_fields = ['title']

    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)
