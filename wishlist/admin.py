from django.contrib import admin
from .models import WishlistItem


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")
    list_filter = ("user", "product")
    search_fields = ("user__username", "product__name")
