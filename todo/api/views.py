from django.http import Http404

from rest_framework.exceptions import PermissionDenied
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
from todo.permissions import IsAdminOrOwnerExceptDelete
from todo.api.serializers import TodoSerializer, LoginSerializer
from todo.mixins import OwnerQuerySetMixin
from todo.api.pagination import TodoCursorPagination
from todo.api.filters import TodoFilter
from todo.throttles import BrustUserThrottle, LoginRateThrottle


@extend_schema(
    tags=["Todos"],
    summary="List & Create Todos",
    description="List user todos or create a new todo",
)
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
        if self.request.user.is_staff:
            return Todo.objects.all().select_related("user")
        return Todo.objects.filter(user = self.request.user).select_related("user").order_by("-created_at")
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


@extend_schema(
    tags=["Todos"],
    summary="Retrieve or Delete Todo",
    description="Retrieve or delete a todo item",
)
class TodoDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        # READ protection
        if not user.is_staff and obj.user != user:
            raise PermissionDenied("You cannot access this todo")

        return obj

    def delete(self, request, *args, **kwargs):
        user = request.user

        # ONLY ADMINS CAN DELETE
        if not user.is_staff:
            raise PermissionDenied("Only admins can delete todos")

        return super().delete(request, *args, **kwargs)


@extend_schema(
    tags=["Auth"],
    summary="User Login",
    description="Login using email and password",
)
class LoginAPIView(APIView):
    throttle_scope = "login"
    throttle_classes = [LoginRateThrottle]
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
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
        }, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Auth"],
    summary="User Login",
    description="Login using email and password",
)
class LogoutAPIView(APIView):
    throttle_scope = "logout"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    
