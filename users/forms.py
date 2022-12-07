from dataclasses import field
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form 
from django import forms
from .models import *
import time



class ReaderCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Reader
        fields = ('email', 'first_name' , 'last_name')

class WriterCreationForm(UserCreationForm):  
    class Meta(UserCreationForm.Meta):
        model = Writer
        fields = ('email', 'first_name' ,'middle_name', 'last_name' , 'password1' , 'password2')
  

class AdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Admin
        fields = ('email', 'first_name' , 'last_name' , 'type')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username' , 'email')

class WriterProfileForm(forms.ModelForm):
    class Meta:
        model = WriterProfile
        fields = ('user', 'image' , 'bio' , 'education', 'nationality')
