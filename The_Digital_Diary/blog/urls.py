from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.post_list, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.publish_post, name='publish_post'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('category/', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_posts, name='category_posts'),
    path('ckeditor/', include('django_ckeditor_5.urls')),
]
