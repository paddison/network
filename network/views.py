import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, PostForm, Post, Likes, Followers


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.user = User.objects.get(id=request.user.id)
            post.save()
            return HttpResponseRedirect(reverse('index'))

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    try:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)
    pst =  Post.objects.get(pk=13)

    try:
        likes = request.user.user.all().values_list('post', flat=True)
    except:
        likes = []
    return render(request, "network/index.html", {
        'PostForm': PostForm(),
        'page_obj': page_obj,
        'likes': likes
    })

@csrf_exempt
@login_required
def like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.get(pk=data['id'])
        try:
            Likes.objects.get(user=request.user, post=post).delete()
            print(f'{request.user} unliked {post}')
            return JsonResponse({
                'liked': False
            })
        except:
            like = Likes(user=request.user, post=post)
            like.save()
            print(f'{request.user} liked{post}')
            return JsonResponse({
                'liked': True
            })
    else:
        return HttpResponseRedirect(reverse('index'))

@csrf_exempt
@login_required
def edit(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        post = Post.objects.get(pk=data['id'])
        if post.user != request.user:
            HttpResponseRedirect(reverse('index'))
        post.text = data['text']
        post.save()
        return JsonResponse({
            "text": post.text
        }, status=200)
    else:
        return HttpResponseRedirect(reverse('index'))

def following(request):
    posts = Post.objects.filter(user__followers__follower=request.user)
    paginator = Paginator(posts, 10)
    try:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)
    try:
        likes = request.user.user.all().values_list('post', flat=True)
    except:
        likes = []
    
    return render(request, "network/following.html", {
        'page_obj': page_obj,
        'likes': likes
    })

def user(request, id):

    userPage = User.objects.get(id=id)

    if request.user.is_authenticated:
        following = request.user.check_follows(id)
    else:
        following = False
    if request.method == 'POST':
        if request.user.check_follows(id):
            #delete
            f = Followers.objects.get(user=userPage, follower=request.user)
            f.delete()
            print('unfollowed')
        else:
            #insert
            follow = Followers(user=userPage, follower=request.user)
            follow.save()
            print('followed')
        
        return HttpResponseRedirect(reverse('user', args=[id]))
    
    posts = Post.objects.filter(user=userPage)
    paginator = Paginator(posts, 10)
    try:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)

    try:
        likes = request.user.user.all().values_list('post', flat=True)
    except:
        likes = []
    return render(request, "network/user.html", {
        'userPage': userPage,
        'page_obj': page_obj,
        'following': following,
        'PostForm': PostForm(),
        'likes': likes
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
