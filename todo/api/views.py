from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema

from todo.selectors.todo_selectors import get_user_todos
from todo.models import Todo
from todo.policies import IsOwner
from todo.api.serializers import TodoSerializer, LoginSerializer
from todo.mixins import OwnerQuerySetMixin
from todo.api.pagination import TodoCursorPagination
from todo.api.filters import TodoFilter


class TodoListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TodoCursorPagination
    filter_backends = [
        DjangoFilterBackend, 
        SearchFilter
    ]
    search_fields = ["title"]
    filterset_class = TodoFilter

    def get_queryset(self):
        if self.request.version == "v2":
            return Todo.objects.filter(
                user = self.request.user,
                is_deleted = False,
            ).select_related("user")
        return Todo.objects.filter(user = self.request.user).order_by("-created_at")
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class TodoDetailAPIView(OwnerQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    queryset = Todo.objects.all()   
    


class LoginAPIView(APIView):
    throttle_scope = "login"
    permission_classes = [permissions.AllowAny]  
    serializer_class = LoginSerializer

    @extend_schema(
            request = {
                "application/json": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string"},
                        "password": {"type": "string"},
                    },
                    "required": ["email", "password"],
                }
            },
            responses = {
                200: {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "user_id": {"type": "integer"},
                    },
                }
            },
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
        }, status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    throttle_scope = "logout"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    
