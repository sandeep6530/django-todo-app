from django.http import Http404
from django.shortcuts import get_object_or_404



class OwnerRequiredMixin:
    model = None
    owner_field = "user"

    def get_object(self, *args, **kwargs):
        if self.model is None:
            raise ImproperlyConfigured(
                "OwnerRequiredMixin requires a model."
            )
        
        obj = get_object_or_404(self.model, pk = self.kwargs.get("pk"))

        if getattr(obj, self.owner_field) != self.request.user:
            raise Http404
        
        return obj
    

class OwnerQuerySetMixin:
    owner_field = "user"

    def get_queryset(self):
        assert hasattr(self, "queryset") or hasattr(self, "model"), (
            "OwnerQuerySetMixin requires queryset and model"
        )
        qs = super().get_queryset()
        return qs.filter(**{self.owner_field: self.request.user})