import uuid
from django.db import models
from django.contrib.auth import models
# Create your models here.

# lets customize our user


class User(models.AbstractUser):
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
    def in_stock(self):
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

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order of {self.quantity} x {self.product.name} on {self.created_at} by {self.user.username}"
