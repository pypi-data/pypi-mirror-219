import django_filters

from dynamic_listing.filters.filters import OrderingFilter, NumberInFilter


class FilterFieldRenderer:
    template_name = ''
    element = None
    single = True

    def __init__(self, filter_field, form_field, value, filter_type='filter'):
        self.name = filter_field.field_name
        self.filter_field = filter_field
        self.filter_type = filter_type
        self.form_field = form_field
        self.value = value

    def is_hidden(self):
        return True

    def get_attrs(self):
        return {
            "name": self.name,
            "value": self.get_value(),
            "label": self.filter_field.label,
            "type": self.element,
            "placeholder": self.form_field.field.widget.attrs[
                'placeholder'] if 'placeholder' in self.form_field.field.widget.attrs else ''
        }

    def get_value(self):
        return self.value

    def get_template_name(self):
        return self.template_name

    def get(self):
        return {
            "element": self.element,
            "template_name": self.get_template_name(),
            "type": self.filter_type,
            "single": self.single,
            "attrs": self.get_attrs()
        }


class NumberInFilterFieldRenderer(FilterFieldRenderer):
    element = 'number'
    single = True

    def get_template_name(self):
        return ''

    def is_hidden(self):
        return False

    def get_value(self):
        return self.form_field.form.data.get(self.name) if self.name in self.form_field.form.data \
            else 0


class BooleanFilterFieldRenderer(FilterFieldRenderer):
    element = 'checkbox'
    single = True

    def get_template_name(self):
        if "data-switch" in self.form_field.field.widget.attrs.keys() \
                and self.form_field.field.widget.attrs["data-switch"]:
            return 'dynamic_listing/filters/fields/switch.html'
        return 'dynamic_listing/filters/fields/checkbox.html'

    def is_hidden(self):
        return False

    def get_attrs(self):
        return {
            **super(BooleanFilterFieldRenderer, self).get_attrs(),
            "checked": self.name in self.form_field.form.data and self.form_field.form.data.get(self.name)
        }

    def get_value(self):
        return 0 if self.name in self.form_field.form.data and self.form_field.form.data.get(self.name) else 1


class CharFilterFieldRenderer(FilterFieldRenderer):
    element = 'text'
    single = True

    def get_template_name(self):
        return 'dynamic_listing/filters/fields/input.html' \
            if self.filter_type != 'search' \
            else 'dynamic_listing/filters/fields/search.html'

    def is_hidden(self):
        return False

    def get_value(self):
        return self.form_field.form.data.get(self.name) if self.name in self.form_field.form.data \
            else ''


class DateTimeFilterFieldRenderer(FilterFieldRenderer):
    template_name = ''


class ChoiceFilterFieldRenderer(FilterFieldRenderer):
    template_name = 'dynamic_listing/filters/fields/radio_group.html'
    single = True
    element = 'radio'

    def is_hidden(self):
        return len([choice for choice in self.form_field.field.choices if choice[0]]) <= 1

    def get_attrs(self):
        return {
            **super(ChoiceFilterFieldRenderer, self).get_attrs(),
            "choices": dict(self.form_field.field.choices)
        }

    def get_value(self):
        return self.form_field.form.data.get(
            self.name) if self.name in self.form_field.form.data and self.form_field.form.data.get(self.name) else None


class ModelChoiceFilterFieldRenderer(FilterFieldRenderer):
    template_name = 'dynamic_listing/filters/fields/radio_group.html'
    single = True
    element = 'radio'

    def is_hidden(self):
        return self.form_field.field.queryset.count() <= 1

    def get_attrs(self):
        return {
            **super().get_attrs(),
            "choices": {str(item.id): str(item) for item in self.form_field.field.queryset}
        }

    def get_value(self):
        return self.form_field.form.data.get(self.name, None)


class ModelMultipleChoiceFilterFieldRenderer(ModelChoiceFilterFieldRenderer):
    template_name = 'dynamic_listing/filters/fields/checkbox_group.html'
    single = False
    element = 'checkbox'

    def is_hidden(self):
        return self.form_field.field.queryset.count() <= 1

    def get_value(self):
        return self.form_field.form.data.getlist(
            self.name) if self.form_field.form.data and self.name in self.form_field.form.data else []


class OrderingFilterRenderer(ChoiceFilterFieldRenderer):
    template_name = 'dynamic_listing/filters/fields/select.html'
    single = True
    element = 'select'

    def is_hidden(self):
        return len(self.form_field.field.choices) <= 1

    def get_attrs(self):
        return {
            **super(ChoiceFilterFieldRenderer, self).get_attrs(),
            "choices": dict(self.form_field.field.choices)
        }

    def get_template_name(self):
        return 'dynamic_listing/filters/fields/select.html' \
            if self.filter_type != 'sort' \
            else 'dynamic_listing/filters/fields/sort.html'


class DateFromToRangeFilterRenderer(FilterFieldRenderer):
    template_name = 'dynamic_listing/filters/fields/date-range.html'

    def is_hidden(self):
        return False

    def get_value(self):
        range_from = self.name + '_from'
        range_to = self.name + '_to'
        value = ''
        if self.form_field.form.data.get(range_from, None) and self.form_field.form.data.get(range_from, None):
            value = self.form_field.form.data.get(range_from, None) + ' - ' + self.form_field.form.data.get(range_to,
                                                                                                            None)
        return {
            "range_from": self.form_field.form.data.get(range_from, None),
            "range_to": self.form_field.form.data.get(range_to, None),
            'value': value
        }


FIELD_RENDERER_MAP = {
    django_filters.filters.BooleanFilter: BooleanFilterFieldRenderer,
    django_filters.filters.CharFilter: CharFilterFieldRenderer,
    django_filters.filters.ChoiceFilter: ChoiceFilterFieldRenderer,
    django_filters.filters.ModelChoiceFilter: ModelChoiceFilterFieldRenderer,
    django_filters.filters.ModelMultipleChoiceFilter: ModelMultipleChoiceFilterFieldRenderer,
    django_filters.filters.DateTimeFilter: DateTimeFilterFieldRenderer,
    django_filters.filters.DateFromToRangeFilter: DateFromToRangeFilterRenderer,
    OrderingFilter: OrderingFilterRenderer,
    NumberInFilter: NumberInFilterFieldRenderer
}
