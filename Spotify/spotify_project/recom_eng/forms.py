from django import forms
from .models import User  # Import the User model

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']  # Include relevant fields
        widgets = {
            'password': forms.PasswordInput(),  # Mask password input
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
