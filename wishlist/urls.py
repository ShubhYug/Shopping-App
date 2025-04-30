from django.urls import path
from .views import WishlistItemListCreateView, WishlistItemDeleteView

urlpatterns = [
    path(
        "wishlist-items/",
        WishlistItemListCreateView.as_view(),
        name="wishlist-item-list-create",
    ),
    path(
        "wishlist-items/delete/<int:pk>/",
        WishlistItemDeleteView.as_view(),
        name="wishlist-item-delete",
    ),
]
