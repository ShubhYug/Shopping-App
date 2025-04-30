from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from .models import CustomUser, OTP
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
import random
import string
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
import datetime
from datetime import timedelta


# without otp
# @api_view(['POST'])
# def register_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        # breakpoint()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                otp_record = OTP.objects.get(email=email)
                otp_value = "".join(random.choices(string.digits, k=6))
                send_mail(
                    "OTP Verification",
                    f"Your OTP is: {otp_value}",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                otp_record.otp = otp_value
                otp_record.save()
                return Response(
                    {"message": "OTP sent successfully.", "otp": otp_record.otp},
                    status=status.HTTP_200_OK,
                )
            except OTP.DoesNotExist:
                otp_value = "".join(random.choices(string.digits, k=6))
                send_mail(
                    "OTP Verification",
                    f"Your OTP is: {otp_value}",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                # otp_record.expires_at = timezone.now() + timedelta(minutes=5) 
                OTP.objects.create(email=email, otp=otp_value)
                return Response(
                    {"message": "OTP sent successfully.", "instructions": otp_value},
                    status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def verify_otp(request):
    if request.method == "POST":
        data = request.data
        email = data.get("email")
        otp_entered = data.get("otp")
        print("data ,,,,,, +++++++++++ ", data)
        print("email ,,,,,, +++++++++++ ", email)
        print("otp_entered ,,,,,, +++++++++++ ", otp_entered)
        if not email or not otp_entered:
            return JsonResponse(
                {"error": "Email address and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # breakpoint()
        try:
            otp_record = OTP.objects.get(email=email)
            print("otp_record ,,,,,, +++++++++++ ", otp_record.otp)
            print("otp_record ,,,,,, +++++++++++ ", otp_record.is_expired)
            if otp_record.otp == otp_entered and not otp_record.is_expired:
                serializer = UserSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    otp_record.delete()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(
                    {
                        "error": f"Incorrect OTP or OTP expired, {otp_record.expires_at}, {otp_record.created_at}, {otp_record.email}, {otp_record.otp}, {timezone.now()}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except OTP.DoesNotExist:
            return JsonResponse(
                {"error": "No OTP record found"}, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
def user_login(request):
    if request.method == "POST":
        email = request.data.get("email")
        password = request.data.get("password")
        # user = None

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if user.check_password(password):
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {"token": token.key, "user": UserSerializer(user).data},
                    status=status.HTTP_200_OK,
                )

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == "POST":
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
