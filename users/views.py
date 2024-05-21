from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserProfileForm, UserUpdateForm
from django.template import loader
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseBadRequest

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        profile_pic = request.FILES.get('profile_pic')
        bio = request.POST['bio']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

 # Create the user
        user = User.objects.create(username=username, email=email, password=make_password(password1))
        UserProfile.objects.create(user=user, profile_pic=profile_pic, bio=bio)

        # Authenticate the user
        user = authenticate(request, username=username, password=password1)

        if user is not None:
            # Login the user
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('home')
        else:
            messages.warning(request, "Failed to authenticate user.")
            return redirect('register')

    return render(request, 'users/register.html')

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def user_details(request, id):
    if request.user.id != id:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')

    user = get_object_or_404(get_user_model(), id=id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user, user=user)
        userprofile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and userprofile_form.is_valid():
            user_form.save()
            userprofile_form.save()
            return redirect('home')
        else:
            context = {
                "user_form": user_form,
                "userprofile_form": userprofile_form,
            }
            return render(request, 'users/details.html', context)
    else:
        user_form = UserUpdateForm(instance=user, user=user)
        userprofile_form = UserProfileForm(instance=user_profile)
    
    context = {
        "user_form": user_form,
        "userprofile_form": userprofile_form,
    }
    return render(request, 'users/details.html', context)