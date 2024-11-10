import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from .models import User, Post, Follower
from .utils import paginate, check_is_valid_uuid


def index(request):
    requested_page_number = request.GET.get("page")
    post_list = Post.objects.order_by("-creation_date")
    own_likes = request.user.own_likes if request.user.is_authenticated else None

    for post in post_list:
        likes_count = post.likes.count()
        is_liked = own_likes.filter(pk=post.id).exists() if request.user.is_authenticated else None
        post.likes_count = likes_count
        post.is_liked = is_liked

    result = paginate(requested_page_number, post_list)
    if "page_error" in result:
        return HttpResponseRedirect(reverse("index"))

    context = {
        "title": "All Posts",
        "posts": result["paginated_posts"],
        "show_new_post_field": True,
        "pagination": result["pagination"],
    }
    return render(request, "network/index.html", context)


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

@login_required()
def create_post(request):
    if request.method == 'POST':
        new_post = request.POST["new-post"]
        Post.objects.create(content=new_post, author=request.user)
        return HttpResponseRedirect(reverse("index"))

def profile(request, username):
    requested_page_number = request.GET.get("page")
    user = User.objects.get(username=username)
    posts = user.own_posts.order_by("-creation_date")

    result = paginate(requested_page_number, posts)
    if "page_error" in result:
        return HttpResponseRedirect(reverse("profile", args=[username]))

    is_following_profile_user = request.user.following.filter(followee=user).exists() if request.user.is_authenticated else None
    followers = user.followers
    following = user.following
    context = {
        "username": username,
        "posts": result["paginated_posts"],
        "posts_count": posts.count(),
        "followers_count": followers.count(),
        "following_count": following.count(),
        "is_following_profile_user": is_following_profile_user,
        "pagination": result["pagination"],
    }
    return render(request, "network/profile.html", context)

@login_required()
def toggle_follow(request):
    if request.method == "POST" and request.POST["follower"] == request.user.username:
        follower = request.POST["follower"]
        followee = request.POST["followee"]
        is_delete_method = request.POST.get("_method") == "DELETE"

        found_follow_relation = Follower.objects.filter(
            follower=User.objects.get(username=follower),
            followee=User.objects.get(username=followee),
        )

        if is_delete_method and found_follow_relation.exists():
            # unfollow
            found_follow_relation.delete()
        elif not is_delete_method and not found_follow_relation.exists():
            # follow
            Follower.objects.create(
                follower=User.objects.get(username=follower),
                followee=User.objects.get(username=followee),
            )
        return HttpResponseRedirect(reverse("profile", args=[followee]))

@login_required()
def following(request): # TO DO: remove useless pagination buttons on following page
    requested_page_number = request.GET.get("page")
    following_users = request.user.following.all().values_list('followee', flat=True)
    posts = Post.objects.filter(author__in=following_users).order_by("-creation_date")

    result = paginate(requested_page_number, posts)
    if "page_error" in result:
        return HttpResponseRedirect(reverse("following"))

    context = {
        "title": "Following", 
        "posts": result["paginated_posts"],
        "show_new_post_field": False,
        "pagination": result["pagination"],
    }
    return render(request, "network/index.html", context)

@login_required()
def edit_post(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id) if check_is_valid_uuid(post_id) else None
        if post:
            post_author = post.author
            if post_author == request.user:
                post.content = data["content"]
                post.last_edit_date = timezone.now()
                post.save()
                return JsonResponse({
                    "id": post.id,
                    "content": post.content,
                    "creationDate": post.creation_date,
                    "lastEditDate": post.last_edit_date,
                }, status=200)
    return HttpResponse(status=400)

@login_required()
def post_likes(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id) if check_is_valid_uuid(post_id) else None
        if post:
            is_liked = data["isLiked"]
            if is_liked:
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            return HttpResponse(status=200)
        return HttpResponse(status=400)