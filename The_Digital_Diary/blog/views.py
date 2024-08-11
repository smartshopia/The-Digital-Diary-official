from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from firebase_config import auth
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from .forms import *
from .signals import *

# Create your views here.

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'profile.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

def about(request):
    return render(request, 'blog/about.html')

def blog(request):
    posts = Post.objects.all()
     # Pagination setup
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    latest_posts = Post.objects.order_by('-published_date')[:10]  # Adjust the number to show more/less posts
   #popular_posts = Post.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')[:3]  # Adjust the number to show more/less posts
    popular_posts = Post.objects.annotate(like_count=models.Count('likes')).order_by('-like_count')[:6]
    context = {
        'posts': posts,
        'latest_posts': latest_posts,
        'popular_posts': popular_posts
    }

    return render(request, 'blog/blog.html', context)

def search(request):
    query = request.GET.get('q')
    # Add search logic here
    return render(request, 'search_results.html', {'query': query})


def contact(request):
    return render(request, 'blog/contact.html')

def settings(request):
    return render(request, 'blog/settings.html')

""" def post_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    latest_posts = Post.objects.order_by('-published_date')[:10]  # Adjust the number to show more/less posts
   #popular_posts = Post.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')[:3]  # Adjust the number to show more/less posts
    popular_posts = Post.objects.annotate(like_count=models.Count('likes')).order_by('-like_count')[:6]
    context = {
        'posts': posts,
        'categories': categories,
        'latest_posts': latest_posts,
        'popular_posts': popular_posts
    }

    return render(request, 'blog/index.html', context) """
def post_list(request):
    # Retrieve all posts (consider optimizing this query)
    all_posts = Post.objects.all()
    
    # Pagination setup
    paginator = Paginator(all_posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Retrieve all categories
    categories = Category.objects.all()
    
    # Retrieve the latest 10 posts ordered by published date
    latest_posts = Post.objects.order_by('-published_date')[:10]
    
    # Retrieve the top 6 most popular posts based on the number of likes
    popular_posts = Post.objects.annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:6]

    # Prepare context data for rendering the template
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'latest_posts': latest_posts,
        'popular_posts': popular_posts
    }

    # Render the template with the context data
    return render(request, 'blog/index.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    new_comment = None

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
        else:
            return redirect('login')
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })


def signup1(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
""" @login_required
def publish_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/publish_post.html', {'form': form}) """

def category_list(request, pk=None):
    print(f"Received pk: {pk}")
    if pk is None:
        # Handle the case where pk is not provided
        pass
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_posts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.all()
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})

@login_required
def publish_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/publish_post.html', {'form': form})

@login_required
def like_post1(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)
#@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
        else:
            # Handle login failure
            pass
    return render(request, 'registration/login.html')

def custom_logout(request):
    logout(request)
    next_page = request.GET.get('next', '/')  # Default to '/' if 'next' is not provided
    return redirect(next_page)

""" def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            messages.success(request, 'Registration successful.')
            return redirect('login')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            request.session['user_id'] = user['idToken']
            messages.success(request, 'Login successful.')
            return redirect('home')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'login.html')

def logout(request):
    try:
        auth.current_user = None
        request.session.flush()
        messages.success(request, 'Logged out successfully.')
    except Exception as e:
        messages.error(request, str(e))
    return redirect('login') """

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/profile.html', context)