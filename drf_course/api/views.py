from django.shortcuts import render
from django.db.models import Max
from .models import Product, Order, OrderItem
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, OrderItemSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


@api_view(['GET', 'POST'])
def ProductList(request):
    products = Product.objects.all()
    productSerializer = ProductSerializer(products, many=True)
    if request.method == 'GET':
        return Response(productSerializer.data)
    elif request.method == 'POST':
        productSerializer = ProductSerializer(data=request.data)
        if productSerializer.is_valid():
            productSerializer.save()
            return Response(productSerializer.data, status=status.HTTP_201_CREATED)
        return Response(productSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ProductDetails(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        productSerializer = ProductSerializer(product)
        return Response(productSerializer.data)

    elif request.method == 'PUT':
        productSerializer = ProductSerializer(product, data=request.data)
        if productSerializer.is_valid():
            productSerializer.save()
            return Response(productSerializer.data)
        return Response(productSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def OrderList(request):
    orders = Order.objects.all()
    orderSerializer = OrderSerializer(orders, many=True)
    if request.method == 'GET':
        return Response(orderSerializer.data)
    elif request.method == 'POST':
        orderSerializer = OrderSerializer(data=request.data)
        if orderSerializer.is_valid():
            orderSerializer.save()
            return Response(orderSerializer.data, status=status.HTTP_201_CREATED)
        return Response(orderSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ProductInfo(request):
    products = Product.objects.all()
    productInfoSerializer = ProductInfoSerializer({
        'products': products,
        'num_of_products': products.count(),
        'max_price_product': products.aggregate(max_price_product=Max('price'))['max_price_product']
        # max_price_product = products.order_by('-price').first()
        # the returned data from the Aggregate() is {"max_price_product": 1000}. so we access this property by saying ["max_price_product"]
    })
    return Response(productInfoSerializer.data, status=status.HTTP_200_OK)
