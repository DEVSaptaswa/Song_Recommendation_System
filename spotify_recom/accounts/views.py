from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    return render(request, 'base.html')

# Sign-Up View
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user to the database
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


# Log-In View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                # Check if the user exists
                user = User.objects.get(username=username)
                # Validate the password
                if user.password == password:
                    login(request, user)  # Log the user in
                    return redirect('dashboard')
                else:
                    messages.error(request, "Password is incorrect")  # Incorrect password
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials")  # Username doesn't exist
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')   # Redirect to the home page or desired URL after logout