from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from functools import wraps

from .models import Cart, Order
from products.models import Product



# ---------------------------------
# BUYER ONLY DECORATOR
# ---------------------------------
def buyer_only(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if (
            not hasattr(request.user, 'userprofile')
            or request.user.userprofile.role != 'buyer'
        ):
            messages.error(
                request,
                "Only buyers allowed ❌"
            )
            return redirect('home')

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper



# ---------------------------------
# ADD TO CART
# ---------------------------------
@login_required
@buyer_only
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:

        cart_item.quantity += 1
        cart_item.save()

        messages.success(
            request,
            "Quantity updated in cart ✅"
        )

    else:

        messages.success(
            request,
            f"{product.name} added to cart 🛒"
        )

    return redirect('cart')



# ---------------------------------
# VIEW CART
# ---------------------------------
@login_required
@buyer_only
def cart_view(request):

    items = Cart.objects.filter(
        user=request.user
    )

    if not items.exists():
        messages.info(
            request,
            "Your cart is empty 🛒"
        )

    total = sum(
        item.total_price()
        for item in items
    )

    return render(
        request,
        'orders/cart.html',
        {
            'items': items,
            'total': total
        }
    )



# ---------------------------------
# CHECKOUT
# ---------------------------------
@login_required
@buyer_only
def checkout(request):

    items = Cart.objects.filter(
        user=request.user
    )

    if not items.exists():

        messages.warning(
            request,
            "Your cart is empty 🛒"
        )

        return redirect('home')


    total = sum(
        item.total_price()
        for item in items
    )


    if request.method == 'POST':

        address = request.POST.get(
            'address'
        )

        if not address:

            messages.error(
                request,
                "Address is required ❌"
            )

            return redirect(
                'checkout'
            )


        # create order
        order = Order.objects.create(
        user=request.user,
        address=address,
        total_price=total
        )


        # clear cart
        items.delete()


        messages.success(
            request,
            f"🎉 Order placed successfully! Order ID: #{order.id}"
        )


        return redirect(
            'home'
        )


    return render(
        request,
        'orders/checkout.html',
        {
            'total': total
        }
    )



# ---------------------------------
# REMOVE CART ITEM
# ---------------------------------
@login_required
@buyer_only
def remove_from_cart(
    request,
    item_id
):

    item = get_object_or_404(
        Cart,
        id=item_id,
        user=request.user
    )

    item.delete()

    messages.success(
        request,
        "Item removed from cart ❌"
    )

    return redirect(
        'cart'
    )



# ---------------------------------
# ORDER HISTORY
# ---------------------------------
@login_required
@buyer_only
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )


    # total of all orders
    total_spent = orders.aggregate(
    Sum('total_price')
    )['total_price__sum'] or 0


    return render(
        request,
        'orders/order_history.html',
        {
            'orders': orders,
            'total_spent': total_spent
        }
    )



# ---------------------------------
# CANCEL ORDER
# ---------------------------------
@login_required
@buyer_only
def cancel_order(
    request,
    order_id
):

    # only POST request allowed
    if request.method != "POST":
        return redirect(
            'order_history'
        )


    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )


    if order.status == 'Pending':

        order.status = 'Cancelled'

        order.save()

        messages.success(
            request,
            "Order cancelled successfully ❌"
        )

    else:

        messages.error(
            request,
            "This order cannot be cancelled"
        )


    return redirect(
        'order_history'
    )