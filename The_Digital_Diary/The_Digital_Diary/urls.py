"""
URL configuration for The_Digital_Diary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('about/',blog_views.about, name='about'),
    path('blog/',blog_views.about, name='blog'),
    path('contact/',blog_views.about, name='contact'),
    path('google_login/', blog_views.google_login, name='google_login'),
    path('google_signup/', blog_views.google_signup, name='google_signup'),
    path('register/', blog_views.register, name='register'),
    path('login/', blog_views.login, name='login'),
    path('logout/', blog_views.logout, name='logout'),
    path('posts_list/', blog_views.post_list, name='post_list'),
    path('accounts/profile/', blog_views.profile, name='profile'),
    #path("upload/", custom_upload_function, name="custom_upload_file"),
    path('ckeditor/', include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
