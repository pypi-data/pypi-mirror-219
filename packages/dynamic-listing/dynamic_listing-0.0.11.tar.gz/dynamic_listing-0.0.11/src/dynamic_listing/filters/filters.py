import django_filters
from django.forms.utils import pretty_name
from django.utils.translation import gettext_lazy as _
from django_filters import BaseInFilter, NumberFilter


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class OrderingFilter(django_filters.OrderingFilter):
    descending_fmt = _('%s Descending')
    ascending_fmt = _('%s Ascending')

    def build_choices(self, fields, labels):
        ascending = [
            (param, labels.get(field, _(pretty_name(param))))
            for field, param in fields.items()
        ]

        descending = [
            ('-%s' % param, labels.get('-%s' % param, self.descending_fmt % label))
            for param, label in ascending
        ]

        ascending = [
            (field, self.ascending_fmt % param)
            for field, param in ascending
        ]

        return [val for pair in zip(ascending, descending) for val in pair]

