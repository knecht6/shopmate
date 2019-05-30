from django.urls import path
from .views import *

urlpatterns = [
    # Department routes
    path('departments/', departments),
    path('department/<int:pk>/', department),
    # Category routes
    path('categories/', categories),
    path('category/<int:pk>/', category),
    path('categories_list/<int:department_id>/', categories_list),
    # Attribute routes
    path('attributes/', attributes),
    path('attribute/<int:pk>/', attribute),
    # Attribute routes
    path('attribute_values/<int:attribute_id>/', attribute_values),
    path('attribute_value/<int:pk>/', attribute_value),
    # Product routes
    path('products_in_category/<int:category_id>/', products_in_category),
    path('products_on_department/<int:department_id>/', products_on_department),
    path('products_on_catalog/', products_on_catalog),
    path('product/<int:pk>/', product),
    path('set_image/<int:pk>/', set_image),
    path('catalog_search/', catalog_search),
    path('create_product_review/', create_product_review),
    path('get_product_reviews/', get_product_reviews),
]