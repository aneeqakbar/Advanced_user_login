from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100 ,label='Enter FirstName')
    last_name = forms.CharField(max_length=100 ,label='Enter LastName')
    email = forms.EmailField(max_length=150, help_text='Enter your Email')
    bio = forms.CharField(max_length=200,widget=forms.Textarea(attrs={'rows':3}) , help_text='Describe yourself')


    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','email', 'password1', 'password2','bio')