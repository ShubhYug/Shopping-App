from rest_framework import generics
from .models import WishlistItem
from .serializers import WishlistItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class WishlistItemListCreateView(generics.ListCreateAPIView):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WishlistItem.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get("product")

        if not product_id:
            return Response(
                {"error": "productId is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Check if the product already exists in the user's wishlist
            wishlist_item = WishlistItem.objects.filter(
                user=user, product=product_id
            ).first()

            if wishlist_item:
                return Response(
                    {"error": "Item already exists in wishlist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                # If the item does not exist, create a new wishlist item
                wishlist_item = WishlistItem.objects.create(
                    user=user, product_id=product_id
                )
                serializer = WishlistItemSerializer(wishlist_item)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WishlistItemDeleteView(generics.DestroyAPIView):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WishlistItem.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
