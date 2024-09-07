from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'id': 'username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email', 'id': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'id': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'id': 'password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio'] 
        