from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            name=validated_data.get("name"),
            address=validated_data.get("address"),
        )
        user.password = make_password(validated_data["password"])
        user.save()
        return user
