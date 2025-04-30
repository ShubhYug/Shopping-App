import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from products.models import Product


@pytest.mark.django_db
class TestProductAPI:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def product(self):
        return Product.objects.create(
            name="Test Product",
            price=99.99,
            description="A sample product",
            shipping_details="Ships in 2 days",
            category="Test Category",
            stock=10,
        )

    def test_create_product(self, client):
        url = reverse("product-list")
        data = {
            "name": "New Product",
            "price": "199.99",
            "description": "Brand new product",
            "shipping_details": "Ships in 3 days",
            "category": "Electronics",
            "stock": 5,
        }
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert Product.objects.filter(name="New Product").exists()

    def test_list_products(self, client, product):
        url = reverse("product-list")
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_get_product_detail(self, client, product):
        url = reverse("product-detail", args=[product.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["name"] == product.name

    def test_update_product(self, client, product):
        url = reverse("product-detail", args=[product.id])
        updated_data = {
            "name": "Updated Product",
            "price": "129.99",
            "description": "Updated description",
            "shipping_details": "Updated shipping",
            "category": "Updated Category",
            "stock": 20,
        }
        response = client.put(url, updated_data, format="json")
        assert response.status_code == 200
        product.refresh_from_db()
        assert product.name == "Updated Product"

    def test_delete_product(self, client, product):
        url = reverse("product-detail", args=[product.id])
        response = client.delete(url)
        assert response.status_code == 204
        assert not Product.objects.filter(id=product.id).exists()
