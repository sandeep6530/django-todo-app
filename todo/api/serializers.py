from rest_framework import serializers

from django.contrib.auth import authenticate
from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "status", "created_at"]
        read_only_fields = ["id", "created_at"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username = data["email"],
            password = data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        return user