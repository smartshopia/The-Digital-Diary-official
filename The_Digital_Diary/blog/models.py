from django.db import models
from django.contrib.auth.models import User
#from tinymce.models import HTMLField
#from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.

class Post1(models.Model):
    title = models.CharField(max_length=200)
    #contenttinMCE = HTMLField()
    content = CKEditor5Field()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    short_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    posts = models.ManyToManyField('Post', related_name='categories_set', blank=True)
    def __str__(self):
        return self.name    
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    is_published = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    short_description = models.CharField(max_length=255, null=True, blank=True)
    content = CKEditor5Field()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='posts_set', blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    share_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)
    #slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title
    def images (self):
        return self.image
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]