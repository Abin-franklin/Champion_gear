from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# 🔥 IMPORT PRODUCT FORM (IMPORTANT)
from products.forms import ProductForm


# ✅ REGISTER
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.models import UserProfile

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Validation
        if not username or not password or not role:
            messages.error(request, "All fields are required ❌")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # Safely get existing profile (from signal) or create one if missing
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Set role and save
        profile.role = role
        profile.save()

        messages.success(request, "Account created successfully ✅")
        return redirect('login')

    return render(request, 'accounts/register.html')


# ✅ LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 Role-based redirect
            role = getattr(user.userprofile, 'role', None)

            if role == 'seller':
                return redirect('add_product')   # go directly to add page
            else:
                return redirect('home')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


# ✅ LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# ✅ ADD PRODUCT (SELLER ONLY)
@login_required
def add_product(request):

    form = ProductForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST":
        if form.is_valid():

            # Don't save directly
            product = form.save(commit=False)

            # Assign owner (required)
            product.seller = request.user

            # Now save
            product.save()

            messages.success(
                request,
                "Product added successfully ✅"
            )

            return redirect('seller_dashboard')

    return render(
        request,
        'products/add_product.html',
        {'form': form}
    )


