from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
from functools import wraps

from .models import Product, Category
from .forms import ProductForm, UserUpdateForm, ProfileUpdateForm
from accounts.models import UserProfile



# ---------------------------------
# HOME
# ---------------------------------
def home(request):

    query = request.GET.get('q','').strip()
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )

    if category_id and category_id.isdigit():
        products = products.filter(
            category_id=int(category_id)
        )

    if min_price and min_price.isdigit():
        products = products.filter(
            price__gte=float(min_price)
        )

    if max_price and max_price.isdigit():
        products = products.filter(
            price__lte=float(max_price)
        )

    if sort == 'low':
        products = products.order_by('price')

    elif sort == 'high':
        products = products.order_by('-price')

    else:
        products = products.order_by('-created_at')


    categories = Category.objects.all()

    return render(
        request,
        'products/home.html',
        {
            'products': products,
            'categories': categories,
            'query': query,
            'selected_category': category_id,
            'min_price': min_price,
            'max_price': max_price,
            'selected_sort': sort,
        }
    )



# ---------------------------------
# SELLER ONLY
# ---------------------------------
def seller_only(view_func):

    @wraps(view_func)
    def wrapper(request,*args,**kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if (
            not hasattr(request.user,'userprofile')
            or request.user.userprofile.role != 'seller'
        ):
            messages.error(
                request,
                "Access Denied ❌ Only sellers allowed"
            )
            return redirect('home')

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper



# ---------------------------------
# ADD PRODUCT
# ---------------------------------
@login_required
@seller_only
def add_product(request):

    form = ProductForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == 'POST':

        if form.is_valid():

            product = form.save(
                commit=False
            )

            product.seller = request.user
            product.save()

            messages.success(
                request,
                "Product added successfully ✅"
            )

            return redirect(
                'seller_dashboard'
            )

    return render(
        request,
        'products/add_product.html',
        {
            'form': form
        }
    )



# ---------------------------------
# SELLER DASHBOARD
# ---------------------------------
@login_required
@seller_only
def seller_dashboard(request):

    products = Product.objects.filter(
        seller=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'products/seller_dashboard.html',
        {
            'products': products
        }
    )



# ---------------------------------
# EDIT PRODUCT
# ---------------------------------
@login_required
@seller_only
def edit_product(request,id):

    product = get_object_or_404(
        Product,
        id=id,
        seller=request.user
    )

    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product
    )

    if request.method == 'POST':

        if form.is_valid():

            updated = form.save(
                commit=False
            )

            updated.seller = request.user
            updated.save()

            messages.success(
                request,
                "Product updated successfully ✏️"
            )

            return redirect(
                'seller_dashboard'
            )

    return render(
        request,
        'products/add_product.html',
        {
            'form': form
        }
    )



# ---------------------------------
# DELETE PRODUCT
# ---------------------------------
@login_required
@seller_only
def delete_product(request,id):

    product = get_object_or_404(
        Product,
        id=id,
        seller=request.user
    )

    product.delete()

    messages.success(
        request,
        "Product deleted successfully 🗑️"
    )

    return redirect(
        'seller_dashboard'
    )



# ---------------------------------
# UPDATE PROFILE
# ---------------------------------
@login_required
def update_profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )


    if request.method == 'POST':

        # -------- Username Update --------
        if 'update_profile' in request.POST:

            u_form = UserUpdateForm(
                request.POST,
                instance=request.user
            )

            p_form = ProfileUpdateForm(
                instance=profile
            )

            pwd_form = PasswordChangeForm(
                user=request.user
            )

            if u_form.is_valid():

                u_form.save()

                messages.success(
                    request,
                    "Username updated successfully ✅"
                )

                return redirect(
                    'update_profile'
                )

            else:

                messages.error(
                    request,
                    "Username update failed ❌"
                )


        # -------- Password Change --------
        elif 'change_password' in request.POST:

            u_form = UserUpdateForm(
                instance=request.user
            )

            p_form = ProfileUpdateForm(
                instance=profile
            )

            pwd_form = PasswordChangeForm(
                user=request.user,
                data=request.POST
            )


            if pwd_form.is_valid():

                user = pwd_form.save()

                update_session_auth_hash(
                    request,
                    user
                )

                messages.success(
                    request,
                    "Password changed successfully 🔐"
                )

                return redirect(
                    'update_profile'
                )
            
            else:
                for field, errors in pwd_form.errors.items():
                    for error in errors:
                        messages.error(
                            request,
                            error
                )

            


    else:

        u_form = UserUpdateForm(
            instance=request.user
        )

        p_form = ProfileUpdateForm(
            instance=profile
        )

        pwd_form = PasswordChangeForm(
            user=request.user
        )


    return render(
        request,
        'users/update_profile.html',
        {
            'u_form': u_form,
            'p_form': p_form,
            'pwd_form': pwd_form
        }
    )