from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Post views added to the admin field
    """
    list_display = ['title','slug','author','publish','status']
    list_filter = ['status','created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status','publish']
    
class CommentAdmin(admin.ModelAdmin):
    """
    Comments added to the admin field
    """
    list_display= ['name', 'email', 'post','created', 'update','activte']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']