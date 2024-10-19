import math
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follower

from .utils import check_is_valid_page_query_param

PAGINATION_LIMIT = 10
MAX_PAGE_BUTTONS = 5
DEFAULT_PAGE = 1

def index(request):
    requested_page_number = request.GET.get("page")
    post_list = Post.objects.order_by("-timestamp")
    paginator = Paginator(post_list, PAGINATION_LIMIT)
    num_pages = paginator.num_pages
    is_valid_page = check_is_valid_page_query_param(requested_page_number, num_pages)

    if requested_page_number and not is_valid_page:
        return HttpResponseRedirect(reverse("index"))

    else:
        page_number = DEFAULT_PAGE if requested_page_number == None else int(requested_page_number)
        page = paginator.page(page_number)
        paginated_posts = page.object_list
        central_page_button_index = math.floor(MAX_PAGE_BUTTONS / 2)
        is_last_window = page_number > (num_pages - ((MAX_PAGE_BUTTONS / 2) - 1))
        first_page_button = (num_pages - MAX_PAGE_BUTTONS) + 1 if is_last_window else max(page_number - central_page_button_index, 1)
        last_page_button = min(first_page_button + (MAX_PAGE_BUTTONS - 1), num_pages)
        page_buttons = range(first_page_button, last_page_button + 1)

        pagination = {
            "is_first_page": page_number == 1,
            "is_last_page": page_number == num_pages,
            "page_buttons": page_buttons,
            "page_number": page_number,
            "previous_page": page_number - 1,
            "next_page": page_number + 1,
        }

        context = {
            "title": "All Posts",
            "posts": paginated_posts,
            "show_new_post_field": True,
            "pagination": pagination,
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
    user = User.objects.get(username=username)
    is_following_profile_user = request.user.following.filter(followee=user).exists() if request.user.is_authenticated else None
    posts = user.own_posts.order_by("-timestamp")
    followers = user.followers
    following = user.following
    context = {
        "username": username,
        "posts": posts,
        "posts_count": posts.count(),
        "followers_count": followers.count(),
        "following_count": following.count(),
        "is_following_profile_user": is_following_profile_user
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
    following_users = request.user.following.all().values_list('followee', flat=True)
    posts = Post.objects.filter(author__in=following_users).order_by("-timestamp")
    context = {"title": "Following", "posts": posts, "show_new_post_field": False}
    return render(request, "network/index.html", context)
