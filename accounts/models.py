from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime
from datetime import timedelta


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username


def default_expiration():
    return timezone.now() + timedelta(minutes=5)


class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiration)

    @property
    def is_expired(self):
        print("default_expiration: ====================", default_expiration)
        print("Expires At: ====================", self.expires_at)
        print("Current Time====================:", timezone.now())
        return timezone.now() > self.expires_at
