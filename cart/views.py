from rest_framework import generics
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    # def post(self, request, *args, **kwargs):
    #     user = request.user
    #     product_id = request.data.get('product')
    #     set_quantity = request.data.get('quantity')

    #     if not product_id:
    #         return Response({'error': 'productId is required'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # Check if the product already exists in the user's cart
    #         cart_item = CartItem.objects.filter(user=user, product=product_id).first()

    #         if cart_item:
    #             # If the item exists, increment the quantity
    #             cart_item.quantity += set_quantity
    #             cart_item.save()
    #             serializer = CartItemSerializer(cart_item)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         else:
    #             # If the item does not exist, create a new cart item with quantity=1
    #             cart_item = CartItem.objects.create(user=user, product_id=product_id, quantity=set_quantity)
    #             serializer = CartItemSerializer(cart_item)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")

        if not product_id:
            return Response(
                {"error": "productId is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {"error": "quantity must be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cart_item = CartItem.objects.filter(
                user=user, product_id=product_id
            ).first()

            if cart_item:
                cart_item.quantity += quantity
                cart_item.save()
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                cart_item = CartItem.objects.create(
                    user=user, product_id=product_id, quantity=quantity
                )
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromCart(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class IncrementQuantity(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.quantity += 1
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DecrementQuantity(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.quantity -= 1
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
