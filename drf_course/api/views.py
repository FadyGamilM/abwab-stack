from django.shortcuts import render
from django.db.models import Max
from .models import Product, Order, OrderItem
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, OrderItemSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
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


class ProductListGenericView(generics.ListAPIView):
    # ! we can alter how the queryset that will be used
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer


class ProductCreateGenericView(generics.CreateAPIView):
    """Generic view for creating products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # We can add any additional logic here before saving
        serializer.save()


class ProductListCreateGenericView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # now we need to allow any for the GET but allow only admin for POST
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        # at the end we call the method of the parent class .. but we need to modify it a little bit
        return super().get_permissions()


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
    # fetch the items and the related products to those items in only one query to avoid the N+1 query problem .. items_product means the product of this item
    orders = Order.objects.prefetch_related('items__product').all()
    orderSerializer = OrderSerializer(orders, many=True)
    if request.method == 'GET':
        return Response(orderSerializer.data)
    elif request.method == 'POST':
        orderSerializer = OrderSerializer(data=request.data)
        if orderSerializer.is_valid():
            orderSerializer.save()
            return Response(orderSerializer.data, status=status.HTTP_201_CREATED)
        return Response(orderSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListGenericView(generics.ListCreateAPIView):
    '''Return the orders of the authenticated user only'''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # in order to handle non-authenticated user insted of app-crashing :
    permission_classes = [IsAuthenticated]

    # ? Dynamic Filtering for the generic class based views
    # filter the orders based on the user
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderDetailsGenericView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'order_id'  # what field to filter based on
    lookup_url_kwarg = 'id'  # the field query param, so these two and ingoring defining the queryset field will query only this order for this auth user so we fetch only one record from db
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


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
