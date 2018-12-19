from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile


def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    if exists:
        raise ValidationError(f"Email address {value} already exists, must be unique")


class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password']


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email_unique])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
