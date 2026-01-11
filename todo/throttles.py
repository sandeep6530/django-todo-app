from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle


class BrustUserThrottle(UserRateThrottle):
    scope = "burst"


class AdminRateThrottle(UserRateThrottle):
    scope = "admin"

    def allow_request(self, request, view):
        if request.user.is_staff:
            return super().allow_request(request, view)
        return True
    
class LoginRateThrottle(ScopedRateThrottle):
    scope = "login"