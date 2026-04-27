from django import forms
from django.contrib.auth.models import User
from .models import Product
from accounts.models import UserProfile



# ---------------------------------
# PRODUCT FORM
# ---------------------------------
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
        'name',
        'category',
        'price',
        'image',
        'description'
    ]



# ---------------------------------
# USER UPDATE FORM
# only username needed now
# ---------------------------------
class UserUpdateForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter username'
            }
        )
    )

    class Meta:
        model = User

        fields = [
            'username'
        ]



# ---------------------------------
# PROFILE FORM
# kept empty because page no longer
# uses phone/address/image
# ---------------------------------
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = []