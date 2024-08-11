from django.contrib import admin
from .models import *
from .forms import *
#from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    #pass
    form = PostForm
    list_display = ('title', 'author', 'display_categories', 'images','created_at', 'published_date', 'is_published')
    filter_horizontal = ('categories',)
    search_fields = ('title', 'content',)
    list_filter = ('published_date', 'author', 'categories',)
    #prepopulated_fields = {"slug": ("title",)}
        
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'  

#class PostInline(admin.TabularInline):
    #model = Post.categories.through  # Use the through model for many-to-many relations
    #extra = 1  # Number of extra forms to display
    #verbose_name = "Related Post"
    #verbose_name_plural = "Related Posts"

class CategoryAdmin(admin.ModelAdmin):
    #inlines = [PostInline]
    list_display = ('name', 'display_categories', 'description')
    filter_horizontal = ('posts',)     
    def display_categories(self, obj):
        return ", ".join([category.title for category in obj.posts.all()])
    display_categories.short_description = 'Categories' 



       
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Profile)
