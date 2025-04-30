import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser, OTP
from django.core import mail


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "phone_number": "1234567890",
        "name": "Test User",
        "address": "Test Address",
    }


@pytest.mark.django_db
def test_register_user_sends_otp(api_client, user_data):
    response = api_client.post(reverse("register"), data=user_data)
    assert response.status_code == 200
    assert "OTP sent successfully." in response.data["message"]
    assert OTP.objects.filter(email=user_data["email"]).exists()
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_verify_otp_creates_user(api_client, user_data):
    # Simulate OTP creation
    otp_obj = OTP.objects.create(email=user_data["email"], otp="123456")

    user_data["otp"] = "123456"
    response = api_client.post(reverse("verify_otp"), data=user_data)
    assert response.status_code == 201
    assert CustomUser.objects.filter(email=user_data["email"]).exists()
    assert not OTP.objects.filter(email=user_data["email"]).exists()


@pytest.mark.django_db
def test_login_valid_credentials(api_client, user_data):
    user = CustomUser.objects.create_user(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
        phone_number=user_data["phone_number"],
        name=user_data["name"],
        address=user_data["address"],
    )

    response = api_client.post(
        reverse("login"),
        {"email": user_data["email"], "password": user_data["password"]},
    )
    assert response.status_code == 200
    assert "token" in response.data


@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    response = api_client.post(
        reverse("login"), {"email": "nonexistent@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_logout(api_client, user_data):
    user = CustomUser.objects.create_user(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
        phone_number=user_data["phone_number"],
        name=user_data["name"],
        address=user_data["address"],
    )
    from rest_framework.authtoken.models import Token

    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    response = api_client.post(reverse("logout"))
    assert response.status_code == 200
    assert response.data["message"] == "Successfully logged out."
