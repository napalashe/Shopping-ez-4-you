from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm

User = settings.AUTH_USER_MODEL


def register_view(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('core:index')
    else:
        form = UserRegisterForm()

    return render(request, 'userauths/sign-up.html', {'form': form})


from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('core:index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid login credentials.')

    else:
        form = AuthenticationForm()

    return render(request, 'userauths/sign-in.html', {'form': form})

@login_required
def account_view(request):
    return render(request, 'userauths/account.html', {'user': request.user})
    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('userauths:account')  
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'userauths/edit-profile.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('userauths:sign-in')
