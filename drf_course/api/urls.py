from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList, name='product-list'),
    path('products/<int:pk>', views.ProductDetails, name='product-details'),
    path('orders/', views.OrderList, name='order-list'),
]
