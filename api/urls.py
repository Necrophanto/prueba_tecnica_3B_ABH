from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.products, name='products'),
    path('inventories/product/<int:product_id>', views.inventories_product, name='inventories_product'),  # /api/inventories/product/{PRODUCT_ID}
    path('orders/', views.orders, name='orders'),
    path('', views.api_fallback, name='api_fallback'),
]
