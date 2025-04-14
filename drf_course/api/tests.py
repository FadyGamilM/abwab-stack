from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order, Product, OrderItem, User
from django.urls import reverse


class OrderListGenericViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='pass1')
        user2 = User.objects.create_user(username='user2', password='pass2')
        order1 = Order.objects.create(user=user1)
        order2 = Order.objects.create(user=user2)
        order3 = Order.objects.create(user=user2)

    def test_user_sees_only_their_orders(self):
        # get the user
        user1 = User.objects.get(username='user1')
        # login with that user
        self.client.force_login(user=user1)
        # call the endpoint
        response = self.client.get(reverse('users-order-list-generic'))
        # assert the result
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User1 should see only 1 order
        self.assertEqual(len(response.data), 1)

        orders = response.json()
        self.assertTrue(
            all(order['user'] == user1.id for order in orders)
        )

    def test_unauthenticated_user_cannot_access_orders(self):
        # Test without authentication
        response = self.client.get(reverse('users-order-list-generic'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
