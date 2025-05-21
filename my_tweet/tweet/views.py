from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
# Import authenticate and logout for custom login/logout views
from django.contrib.auth import login, authenticate, logout
# Import Django's default AuthenticationForm for the custom login view
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages # For displaying messages to the user
# Create your views here.
def index(request):
    return render(request,'tweet/index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet/tweet_list.html', {'tweets' : tweets})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request,'tweet/tweet_form.html',{'form':form})

@login_required
def tweet_edit(request, id):
    tweet = get_object_or_404(Tweet, pk=id, user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request,'tweet/tweet_form.html',{'form':form})

@login_required
def tweet_delete(request, id):
    tweet = get_object_or_404(Tweet, pk=id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet/tweet_confirm_delete.html',{'tweet' : tweet})

def register_form(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request,'Registrations/register.html',{'form':form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!') # Add a success message
                return redirect('tweet_list') # Redirect to tweet list after successful login
            else:
                messages.error(request, 'Invalid username or password.') # Add an error message
        else:
            messages.error(request, 'Invalid username or password.') # For form validation errors
    else:
        form = AuthenticationForm()
    return render(request, 'Registrations/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.') # Add an info message
    return redirect('tweet_list') # Redirect to tweet list after logout