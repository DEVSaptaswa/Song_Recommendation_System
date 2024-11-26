from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Retrieve authenticated user
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')   # Redirect to the home page or desired URL after logout