from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList, name='product-list'),
    path('products/v2/', views.ProductListGenericView.as_view(),
         name='product-list-generic'),
    path('products/<int:pk>', views.ProductDetails, name='product-details'),
    path('orders/', views.OrderList, name='order-list'),
    path('orders/v2/<uuid:id>/', views.OrderDetailsGenericView.as_view(),
         name='order-details-generic'),
    path('users-orders/v2/', views.OrderListGenericView.as_view(),
         name='users-order-list-generic'),
    path('products/product-info',
         views.ProductInfo, name='product-info'),
    path('products/create/', views.ProductCreateGenericView.as_view(),
         name='product-create'),
    path('products/v2/', views.ProductListCreateGenericView.as_view(),
         name='product-list-create-generic'),
]
