from django.urls import path
from . import views


urlpatterns = [

    # ---------------------------------
    # HOME
    # ---------------------------------
    path(
        '',
        views.home,
        name='home'
    ),


    # ---------------------------------
    # SELLER DASHBOARD
    # ---------------------------------
    path(
        'seller-dashboard/',
        views.seller_dashboard,
        name='seller_dashboard'
    ),


    # ---------------------------------
    # PRODUCT CRUD
    # ---------------------------------
    path(
        'add-product/',
        views.add_product,
        name='add_product'
    ),

    path(
        'edit-product/<int:id>/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'delete-product/<int:id>/',
        views.delete_product,
        name='delete_product'
    ),


    # ---------------------------------
    # PROFILE
    # ---------------------------------
    path(
        'profile/update/',
        views.update_profile,
        name='update_profile'
    ),

]