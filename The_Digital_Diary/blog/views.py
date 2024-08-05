from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .firebase_config import auth
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .forms import *

# Create your views here.

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

def about(request):
    return render(request, 'blog/about.html')

def post_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    latest_posts = Post.objects.order_by('-published_date')[:3]  # Adjust the number to show more/less posts
   #popular_posts = Post.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')[:3]  # Adjust the number to show more/less posts
    popular_posts = Post.objects.annotate(like_count=models.Count('likes')).order_by('-like_count')[:3]
    context = {
        'posts': posts,
        'categories': categories,
        'latest_posts': latest_posts,
        'popular_posts': popular_posts
    }

    return render(request, 'blog/index.html', context)
    return render(request, 'blog/index.html', {'latest_posts': latest_posts, 'categories': categories, 'popular_posts': popular_posts})

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
@login_required
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
def register(request):
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
    return redirect('login')

def google_login(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        id_token = data.get('idToken')
        try:
            user = auth.sign_in_with_id_token(id_token)
            # Implement your login logic here, e.g., create a session or user model
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False}, status=400)
    return JsonResponse({'success': False}, status=400)

def google_signup(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        id_token = data.get('idToken')
        try:
            user = auth.sign_in_with_id_token(id_token)
            # Implement your signup logic here, e.g., create a user record
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False}, status=400)
    return JsonResponse({'success': False}, status=400)