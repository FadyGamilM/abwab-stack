from rest_framework import serializers
from .models import User, Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        # the order, product are FKs, so how this will be represented in the output of the serialzer
        fields = ['order', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    # The order consists of multiple orderItems .. so we need to define the serializer of the orerItem as a nested serializer in here .. and we mark it as readonly field so we populate it when we return but not expect it in the input
    items = OrderItemSerializer(many=True, read_only=True)

    # we defined a property in the OrderItem model to calculate the orderItemSubtota = product.price * qty
    # but we need to calculate the total order price which will be the sum of the entire subtotal of all OrderItems .. and to add this extra field, we can add it here as a serialization field instead of adding it to the model class
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        '''The obj field is the model we are working with (Order)'''
        total = 0
        for item in obj.items.all():
            total += item.order_item_subtotal
        return total

    class Meta:
        model = Order
        # the user is a FK, so how this will be represented in the output of the serialzer
        fields = ['order_id', 'status', 'user',
                  # we added the extra field of the serializer into the fields that will be exposed to the view handler.
                  'created_at', 'updated_at', 'items', 'total_price']


class ProductInfoSerializer(serializers.Serializer):
    '''This is an example of how to define a dto/serializer to hold data that doesn't need to be tied to a db model'''
    products = ProductSerializer(many=True)
    num_of_products = serializers.IntegerField()
    max_price_product = serializers.FloatField()
