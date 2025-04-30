from django.test import TestCase

# Create your tests here.
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from cart.models import CartItem
from products.models import Product
from accounts.models import CustomUser


@pytest.mark.django_db
class TestAddToCart:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create_user(
            username="testuser", password="testpass"
        )

    @pytest.fixture
    def product(self):
        return Product.objects.create(name="Test Product", price=100)

    def test_add_new_cart_item(self, client, user, product):
        client.force_authenticate(user=user)
        url = reverse("add-to-cart")
        data = {"product": product.id, "quantity": "2"}
        response = client.post(url, data)
        assert response.status_code == 201
        assert CartItem.objects.filter(user=user, product=product).exists()

    def test_increment_existing_cart_item(self, client, user, product):
        CartItem.objects.create(user=user, product=product, quantity=1)
        client.force_authenticate(user=user)
        url = reverse("add-to-cart")
        data = {"product": product.id, "quantity": "2"}
        # breakpoint()
        response = client.post(url, data)
        assert response.status_code == 200
        cart_item = CartItem.objects.get(user=user, product=product)
        assert cart_item.quantity == 3
