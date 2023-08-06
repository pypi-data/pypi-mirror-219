from django import template

register = template.Library()


def find(filters, filter_type):
    return [item for item in filters if item['type'] == filter_type]


@register.filter
def get_first_filter_by_type(filters, filter_type):
    result = find(filters, filter_type)
    return result[0] if len(result) else False


@register.filter
def get_filters_by_type(filters, filter_type):
    return find(filters, filter_type)
