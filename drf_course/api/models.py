import uuid
from django.db import models
from django.contrib.auth import models as auth_models
# Create your models here.

# lets customize our user


class User(auth_models.AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def in_stock(self) -> bool:
        return self.stock > 0


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        SHIPPED = 'Shipped'
        CONFIRMED = 'Confirmed'
        DELIVERED = 'Delivered'
        CANCELED = 'Canceled'

    order_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, blank=True)

    # the relationship btn order and product is many-to-many because order contains multiple products and same product-type can be ordered multiple times in different orders
    products = models.ManyToManyField(
        # related_name is the name to access the products from the order object by saying order.products directly
        Product, through='OrderItem', related_name='orders')

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username} ({self.status})"


class OrderItem(models.Model):
    # one-to-many as one order contains many orderItems so put the one at the many
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    # the reason i defined a through field in the relationship btn the Product <> Order is to include extra details in this relation for example the qty
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.order.order_id}"

    @property
    def order_item_subtotal(self):
        return self.product.price * self.quantity
