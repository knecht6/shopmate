from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    # Customer routes
    path('api/token/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('register_customer/', register_customer),
    path('customer/', customer),
    path('customer_update_address/', customer_update_address),
    path('customer_update_credit_card/', customer_update_credit_card),
    # Shopping Cart routes
    path('shopping_cart_add_product/', shopping_cart_add_product, name='shopping_cart_add_product'),
    path('shopping_cart_update/', shopping_cart_update, name='shopping_cart_update'),
    path('shopping_cart_create_order/', shopping_cart_create_order, name='shopping_cart_create_order'),
    path('shopping_cart_get_products/', shopping_cart_get_products),
    path('shopping_cart_get_saved_products/', shopping_cart_get_saved_products),
    path('shopping_cart_remove_product/', shopping_cart_remove_products, name='shopping_cart_remove_products'),
    path('shopping_cart_save_product_for_later/', shopping_cart_save_product_for_later),
    path('shopping_cart_move_product_to_cart/', shopping_cart_move_product_to_cart),
    # Order routes
    path('orders_get_by_customer_id/', orders_get_by_customer_id),
    path('get_order_details/', get_order_details),
    path('get_order_info/', get_order_info),
    path('get_order_short_details/', get_order_short_details),
    path('get_shipping_options/', get_shipping_options),
]