from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
import pycountry
from django import forms
from django_countries.fields import CountryField
#from .signals import *
#from tinymce.models import HTMLField
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    #location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = CountryField(blank_label='(select country)')
    state = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6),
    longitude = models.DecimalField(max_digits=9, decimal_places=6),
    # Add any other fields you want

    @property
    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return '/media/profile_pictures/tdd.jpg'

    def __str__(self):
        return f'{self.user.username} Profile'
    def __str__(self):
        return self.user.username

class LocationForm(forms.Form):
    country = forms.ChoiceField(
        choices=[(country.alpha_2, country.name) for country in pycountry.countries],
        required=True,
        label="Select Country"
    )
class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.name}, {self.country.name}"  

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
    image = models.ImageField(upload_to='post_images/', null=False, blank=False)
    categories = models.ManyToManyField(Category, related_name='categories_set', blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    share_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    #slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        # Update short_description to be the first 255 characters of stripped content
        if self.content:
            plain_text_content = strip_tags(self.content)
            self.short_description = plain_text_content[:255]
        super().save(*args, **kwargs)
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