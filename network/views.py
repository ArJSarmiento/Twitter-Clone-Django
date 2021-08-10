from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
import time, datetime
from django.http import JsonResponse
from django import forms
from .models import User, Post, Followers
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

class PostForm(forms.ModelForm):
    caption = forms.CharField( 
        label='', 
        widget= forms.TextInput (attrs=
        {
            'class':'captionform',
            'id':'captionform',
            'placeholder':"What's happening?"
        }))

    class Meta:
        model = Post
        fields = ['caption']

@csrf_exempt
def index(request):
    follower_posts = [post for post in Post.objects.all()]    
    follower_posts.sort(key=lambda x: x.datetime, reverse=True)
    paginator = Paginator(follower_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        "postform" : PostForm(),
        'page_obj': page_obj
    }
    return render(request, 'network/index.html', data)

@csrf_exempt
def following(request):
    current_user = request.user 
    follower_posts = [post for post in Post.objects.all()]

    if current_user.is_authenticated:
        _me = Followers.objects.get(me = current_user)
        followers =  _me.my_following.all()
        follower_posts = [post for follower in followers for post in Post.objects.filter(poster = follower)]
        
    follower_posts.sort(key=lambda x: x.datetime, reverse=True)
    paginator = Paginator(follower_posts, 10)

    # data =  json.loads(serializers.serialize('json', follower_posts)) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        "postform" : PostForm(),
        'page_obj': page_obj
    }
    return render(request, 'network/index.html', data)

@csrf_exempt
def profile(request, profile_id):
    current_user = request.user
    user_profile = User.objects.get(id = profile_id)

    user_posts =  [x for x in Post.objects.filter(poster = user_profile)]
    user_posts.sort(key=lambda x: x.datetime, reverse=True)

    following = len([y for y in Followers.objects.get(me = user_profile).my_following.all()])
    followers = len( [i for i in Followers.objects.filter(my_following = user_profile)])

    paginator = Paginator(user_posts, 10)

    # data =  json.loads(serializers.serialize('json', follower_posts)) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        "user_profile":user_profile,
        "page_obj" : page_obj,
        "followers":followers,
        "following": following
    }
    return render(request, 'network/profile.html', data)

@csrf_exempt
@login_required
def add_post(request):  
    data = json.loads(request.body)
    post_caption  = data.get("caption")
    current_user = request.user

    if post_caption == [""]:
            return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    added_post = Post(
        datetime = datetime.datetime.now(),
        caption = post_caption,
        poster = current_user
        
    )
    added_post.save()
    return JsonResponse({"message": "Post sent successfully."}, status=201)


@login_required
@csrf_exempt
def follow_status(request , status_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    current_user = request.user
    user_profile = User.objects.get(id = status_id)
    _me = Followers.objects.get(me = current_user)
    
    response_data = {}
    if user_profile in _me.my_following.all():
        response_data['result'] = 'success'
    else:
        response_data['result'] = 'failed'

    return JsonResponse(response_data)
    
@csrf_exempt
@login_required
def follow_user(request, follow_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    current_user = request.user
    user_profile = User.objects.get(id = follow_id)
    _me = Followers.objects.get(me = current_user)
    
    response_data = {}
    if user_profile in _me.my_following.all():
        _me.my_following.remove(user_profile)
    else:
        _me.my_following.add(user_profile)

    return JsonResponse({"message": "User Followed."}, status=201)

@csrf_exempt
@login_required
def edit_post(request, edit_id):
    data = json.loads(request.body)
    post_caption  = data.get("caption")
    posttoedit = Post.objects.get(id=edit_id)

    if post_caption == [""]:
            return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    posttoedit.caption=post_caption
    posttoedit.save()
    return JsonResponse({"message": "Post edited successfully."}, status=201)

@csrf_exempt
def is_mypost(request, post_id):
    current_user = request.user
    if request.method != "POST" or current_user is None:
        return JsonResponse({"error": "POST request required."}, status=400)

    _poster =  Post.objects.get(id = post_id).poster
    response_data = {'result': 'success' if current_user == _poster else 'failed'}
    return JsonResponse(response_data)

@csrf_exempt
def is_liked(request, islike_id):
    current_user = request.user
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    _poster =  Post.objects.get(id = islike_id)
    likes = _poster.likes.all()
    response_data = {
        "likecount": likes.count(),
        'result': 'success' if current_user in likes else 'failed',
    }

    return JsonResponse(response_data)

@csrf_exempt
@login_required
def like_post(request, like_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    current_user = request.user
    posttolike = Post.objects.get(id = like_id)
    
    response_data = {}
    if current_user in posttolike.likes.all():
        posttolike.likes.remove(current_user)
    else:
        posttolike.likes.add(current_user)
        
    return JsonResponse({"message": "Post liked successfully."}, status=201)


def login_view(request):
    if request.method != "POST":
        return render(request, "network/login.html")

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

        # Check if authentication successful
    if user is None:
        return render(request, "network/login.html", {
            "message": "Invalid username and/or password."
        })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))


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

            f = Followers(me = user)
            f.save()
            
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
