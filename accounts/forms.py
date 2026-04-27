from django import forms
from django.contrib.auth.models import User
from .models import Product
from accounts.models import UserProfile

ROLE_CHOICES = (
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']