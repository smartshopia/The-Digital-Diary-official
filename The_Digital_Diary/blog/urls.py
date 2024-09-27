from django.urls import path, include
from django.conf import global_settings  # This would override the correct settings from django.con
from django.conf.urls.static import static
from . import views
from .views import *

urlpatterns = [
    path('', views.post_list, name='home'),
    path('example1', views.example1, name='example1'),
    path('example2', views.example2, name='example2'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.publish_post, name='publish_post'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/share/', views.share_post, name='share_post'),
    path('categories/<int:pk>/', views.category_posts, name='category_posts'),
    path('ckeditor/', include('django_ckeditor_5.urls')),
    path('about/', about, name='about'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
    path('publish/', publish_post, name='publish_post'),
    path('publish_info/', publish_post_info, name='publish_post_info'),
    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    path('categories/', category_list, name='category_list'),
    path('search/', search, name='search'),
    path('subscribe/', subscribe, name='subscribe'),
]
if global_settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
