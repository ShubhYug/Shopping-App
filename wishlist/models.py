from django.db import models
from accounts.models import CustomUser
from products.models import Product


class WishlistItem(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="wishlist_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="wishlist_items", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username}'s Wishlist Item - {self.product.name}"
