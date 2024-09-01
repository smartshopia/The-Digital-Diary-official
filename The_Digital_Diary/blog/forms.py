from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries.widgets import CountrySelectWidget
#from tinymce.widgets import TinyMCE
from .models import *

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'placeholder': 'Enter your email'})
        }

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'birth_date', 'country', 'state', 'city', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
                if 'state' in self.data:
                    state_id = int(self.data.get('state'))
                    self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.state_set.order_by('name')
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

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

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model =  Profile
        fields = ('user', 'email', 'password1', 'password2', 'profile_picture', 'bio',  'country','state', 'city')

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