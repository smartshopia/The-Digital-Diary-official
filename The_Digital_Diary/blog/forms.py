from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries.widgets import CountrySelectWidget
#from tinymce.widgets import TinyMCE
from .models import *

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'birth_date', 'country','state', 'city']
        widgets = {
            'country': CountrySelectWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class PostForm(forms.ModelForm):
    #content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Post
        fields = ['title','author', 'content', 'image','is_published', 'categories']
  
class PostAdminForm(forms.ModelForm):
    #content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Post
        fields = ['title','author', 'content', 'image', 'short_description','likes','share_count','is_published', 'categories']
  
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'autocapitalize': 'none',
            'autocomplete': 'username',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control'
        })
    )        