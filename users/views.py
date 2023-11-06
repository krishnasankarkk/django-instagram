from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as logout_user
from django.contrib import messages

from .forms import LoginForm, RegistrationForm
from .models import UserAccount
from posts.models import Post

def login_view(request):
    # if request.method == "POST":
    #    form = LoginForm(request, data=request.POST)
       
    #    if form.is_valid():
    #        username = request.POST["username"]
    #        password = request.POST["password"]
    #        user = authenticate(request, username=username, password=password)
    #        if user is not None:
    #            login(request, user)
    #        else:
    #            form.add_error(None, 'Invalid username or passwprd!')
    # else:
    #     form = LoginForm()
        
    # context = {"form":form}
    return render(request, "users/login.html")

def signup(request):
    form = RegistrationForm()
    context = {"form":form}
    return render(request, "users/signup.html", context)
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        fullname = request.POST.get('fullname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            messages.warning(request,"User already exists!")
            return redirect("users:signup")
        except:    
            new_user = User()
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.save()
            new_user_account = UserAccount()
            new_user_account.user = new_user
            new_user_account.save()
            return redirect("users:login")
            
    
    
# @login_required
# def home(request):
#     return render(request, "home.html")

@login_required
def profile(request):
    login_user = request.user.id
    account = UserAccount.objects.get(user_id=login_user)
    followers = len(account.followers) if account.followers is not None else 0
    following = len(account.following) if account.following is not None else 0
    posts = Post.objects.filter(user_id=login_user)
    context = {
        "account_details":account,
        "posts":posts,
        "followers":followers,
        "following":following,
    }
    return render(request, "users/profile.html", context)

def user_profile(request, user_id):
    user_account = UserAccount.objects.get(user_id=user_id)
    followers = len(user_account.followers) if user_account.followers is not None else 0
    following = len(user_account.following) if user_account.following is not None else 0
    if user_account.followers is not None and request.user.id in user_account.followers: 
        followed = True
    else:
        followed = False
    posts = Post.objects.filter(user_id=user_id)
    context = {
        "account_details":user_account,
        "posts":posts,
        "followed":followed,
        "followers":followers,
        "following":following,
    }
    return render(request, "users/user-profile.html", context)

def create(request):
    return render(request, "base.html")

def logout(request):
    logout_user(request)
    return redirect("users:login")

@login_required
def follow_user(request, user_id):
    user_to_follow = UserAccount.objects.get(user_id=user_id)
    current_user = UserAccount.objects.get(user_id=request.user.id)
    if user_to_follow.followers is not None and current_user.user_id in user_to_follow.followers:
        return JsonResponse({'status': 'fail'}) 
    else:
        user_to_follow.followers.append(current_user.user_id)
        user_to_follow.save()
        current_user.following.append(user_to_follow.user_id)
        current_user.save()
        previous_url = request.META.get('HTTP_REFERER', None)
        return HttpResponseRedirect(previous_url)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = UserAccount.objects.get(user_id=user_id)
    current_user = UserAccount.objects.get(user_id=request.user.id)
    if user_to_unfollow.followers is not None and current_user.user_id in user_to_unfollow.followers:
        user_to_unfollow.followers.remove(current_user.user_id)
        user_to_unfollow.save()
        current_user.following.remove(user_to_unfollow.user_id)
        current_user.save()
        previous_url = request.META.get('HTTP_REFERER', None)
        return HttpResponseRedirect(previous_url)
    else:
        return JsonResponse({'status': 'fail'}) 