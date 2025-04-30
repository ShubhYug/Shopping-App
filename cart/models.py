from django.db import models
from accounts.models import CustomUser
from products.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="cart_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="cart_items", on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Cart Item - {self.product.name}"
