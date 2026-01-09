import django_filters
from todo.models import Todo


class TodoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")
    is_deleted = django_filters.BooleanFilter()

    class Meta:
        model = Todo
        fields = ["status", "is_deleted"]