from django.contrib import admin
from django.contrib.auth import views as auth_views
import debug_toolbar
from django.urls import path, include
from django.http import JsonResponse

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

def health_check(request):
    return JsonResponse({ "status": "ok" })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),

    path("", include("todo.urls")),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("__debug__", include(debug_toolbar.urls)),
    
    path("api/<str:version>/", include("todo.api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    # path("api/redoc/", SpectacularRedocView.as_view(url_name="schema")),
]
