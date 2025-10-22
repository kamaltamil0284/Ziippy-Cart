from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserForm(UserCreationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'placeholder':'Enter your name'}))
    email = forms.EmailField(label='E-Mail',widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'placeholder':'Re-enter password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['address', 'mobile']