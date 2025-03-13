from rest_framework import serializers
from user.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "username"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": False},
        }

    def create(self, validated_data):
        if "username" not in validated_data or not validated_data["username"]:
            validated_data["username"] = validated_data["email"].split("@")[0]
        
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
