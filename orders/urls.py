from django.urls import path
from . import views

urlpatterns = [
    # 🛒 Cart
    path('cart/', views.cart_view, name='cart'),

    # ➕ Add to Cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # 💳 Checkout
    path('checkout/', views.checkout, name='checkout'),

    # ❌ Remove item
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('my-orders/', views.order_history, name='order_history'),
    path(
    'cancel-order/<int:order_id>/',
    views.cancel_order,
    name='cancel_order'
),
]