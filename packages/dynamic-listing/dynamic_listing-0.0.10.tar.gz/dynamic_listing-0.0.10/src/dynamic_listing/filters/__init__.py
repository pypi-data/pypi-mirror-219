from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .filter_field_renderer import *
from .filter_renderer import *
from .filters import *


class FilterSet(django_filters.FilterSet):
    filterset_types = {}
    force_visibility = []
    filterset_renderer = FilterRenderer

    RATE_CHOICES = (
        (4, mark_safe('<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '{}'.format(_(" & Up")))),
        (3, mark_safe('<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '{}'.format(_(" & Up")))),
        (2, mark_safe('<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '{}'.format(_(" & Up")))),
        (1, mark_safe('<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '{}'.format(_(" & Up"))))
    )

    def get_renderer(self):
        return self.filterset_renderer(self, self.get_filterset_types()).as_fields()

    def get_filterset_types(self):
        return self.filterset_types

    def filter_boolean(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: value})
        return queryset

    def filter_rate(self, queryset, name, value):
        if not value:
            return queryset
        value = int(value)
        lookup = {}
        if value == 1:
            lookup = {name + "__lt": 2, name + "__gte": 1}
        elif value == 2:
            lookup = {name + "__lt": 3, name + "__gte": 2}
        elif value == 3:
            lookup = {name + "__lt": 4, name + "__gte": 3}
        elif value == 4:
            lookup = {name + "__lte": 5, name + "__gte": 4}

        return queryset.filter(**lookup)
