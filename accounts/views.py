from django.shortcuts import render, redirect
from .forms import RegisterUser, ProfileUpdate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profile
from django.contrib.auth.decorators import login_required
from django_countries import countries
# Create your views here.

def create_user(request):
    form = RegisterUser()
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists ')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                # return redirect('accounts:signup')
            elif password1 != password2:
                messages.error(request, 'Password mismatch')
            elif len(password1) < 5:
                messages.error(request, 'Password most be more than 5 characters')
            else: 
                form.save()
                messages.success(request, 'User created successfully')
                return redirect('accounts:login')
        else:
            messages.error(request, 'Form validation failed')
    else:
        form = RegisterUser()
    return render(request, 'accounts/signup.html', {'form': form})
        
        
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'user login successfully')
            return redirect('core:home')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'user logout successfully')
    return redirect('accounts:login')

@login_required
def user_profile(request):
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    choices = Profile.JOB_STATUS
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdate(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            var.save()
            messages.info(request, "Profile Updated successfully")
            return redirect('accounts:profile')
        else:
            messages.error(request, 'something went wrong')
    else:
        form = ProfileUpdate(instance=profile)
    context = {
        'form': form,
        'choices': choices,
     'profile':profile, 
     'countries':countries}
    return render(request, 'accounts/edit_profile.html', context)