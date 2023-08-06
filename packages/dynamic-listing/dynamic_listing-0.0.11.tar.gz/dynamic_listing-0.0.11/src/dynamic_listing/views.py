import random
import string

from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from django.views.generic.list import MultipleObjectMixin
from django_filters.views import FilterView

"""
    - listing types: table, list, grid
    - filters: side_filters, search
    - statistics: 
    - bulk actions: 
    - charts: 
    - actions: 
    - breadcrumb:
    - title: 
    - sorting:
"""


class DynamicListInit:
    def __init__(self, request=None, queryset=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.queryset = queryset
        self.request = request
        self.object_list = self.get_queryset()


class BaseList(MultipleObjectMixin):
    queryset = None
    request = None
    listing_type = ''
    model = None
    paginate_by = 10
    filterset_class = None
    filterset_renderer = None
    listing_actions = None
    modals_template_name = None
    load_actions_from_template = False
    listing_template_name = None
    header_template_name = None
    factory = False
    has_bulk_actions = False

    def __init__(self, *args, **kwargs):
        source = string.ascii_letters + string.digits
        self.id = ''.join((random.choice(source) for i in range(8)))

        if self.extra_context is None:
            self.extra_context = {}

        self.media = {"css": [], 'js': []}

        super(BaseList, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.render()

    def get_queryset(self):
        queryset = super(BaseList, self).get_queryset()
        if self.filterset_class:
            filters, self.filterset_renderer = self.get_filter(queryset)
            queryset = filters.qs
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(BaseList, self).get_context_data(*args, **kwargs)
        context['request'] = self.request
        context['list_id'] = self.id
        context['actions'] = self.get_listing_actions()
        context['filter'] = self.filterset_renderer
        context['listing_type'] = self.listing_type
        context['has_bulk_actions'] = self.has_bulk_actions
        context['media'] = self.get_media()
        context['factory'] = self.factory
        context['listing_template_name'] = self.listing_template_name
        if self.modals_template_name:
            context['modals_template_name'] = self.modals_template_name
        if self.header_template_name:
            context['header_template_name'] = self.header_template_name
        return context

    def get_listing_actions(self):
        return self.listing_actions

    def get_media(self):
        return mark_safe(self.get_js() + self.get_css())

    def get_js(self):
        self.media['js'].append('dynamic_listing/filters.js')

        js = ''

        if 'js' not in self.media:
            return js

        for item in self.media['js']:
            js += '<script src="{}"></script>'.format(static(item))

        return js

    def get_css(self):
        css = ''
        if 'css' not in self.media:
            return css

        for item in self.media['css']:
            css += '<link href="{}">'.format(static(item))
        return css

    def get_filter(self, queryset):
        if self.filterset_class:
            filters = self.filterset_class(self.request.GET, queryset)
            return filters, filters.get_renderer
        return None, None

    def render(self):
        return mark_safe(render_to_string(self.listing_template_name, self.get_context_data()))


class DynamicTable(BaseList):
    listing_type = 'table'
    table_columns = ()
    load_rows_from_template = False
    row_template_name = None
    actions_template_name = None
    empty_listing_actions_template_name = None
    listing_template_name = 'dynamic_listing/_table_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DynamicTable, self).get_context_data(*args, **kwargs)
        context['columns'] = self.process_table_columns()
        context['load_rows_from_template'] = self.load_rows_from_template
        if self.load_rows_from_template:
            context['row_template_name'] = self.row_template_name
        else:
            context['rows'] = self.load(context['object_list'])

        if self.load_actions_from_template:
            context['actions_template_name'] = self.actions_template_name

        return context

    def load(self, object_list):
        items = []
        for item in object_list:
            items.append(self._load_object_row(item))
        return items

    def _load_object_row(self, obj):
        row = []
        for column_name, text in self.get_table_columns():
            method = "load_{}".format(column_name)
            if hasattr(self, method) and callable(getattr(self, method)):
                call = getattr(self, method)
                row.append(call(obj))
            else:
                row.append(mark_safe('<td>{}</td>'.format(getattr(obj, column_name))))
        return row

    def process_table_columns(self):
        columns = []
        for column in self.get_table_columns():
            columns.append((column[0], column[1], column[2] if len(column) > 2 else ''))
        return columns

    def get_table_columns(self):
        return self.table_columns


class DynamicGrid(BaseList):
    listing_type = 'grid'
    grid_item_template_name = None
    item_template_name = None
    listing_actions_template_name = None
    listing_template_name = 'dynamic_listing/_grid.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DynamicGrid, self).get_context_data(*args, **kwargs)
        context['item_template_name'] = self.item_template_name
        return context


class DynamicList(BaseList):
    listing_type = 'grid'
    item_template_name = None
    listing_actions_template_name = None
    listing_template_name = 'dynamic_listing/_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DynamicList, self).get_context_data(*args, **kwargs)
        context['item_template_name'] = self.item_template_name
        return context


def dynamic_table_factory(model, dynamic_list=DynamicTable, filterset_class=None, listing_type='table',
                          listing_actions=None, table_columns=None, load_rows_from_template=False,
                          row_template_name=None, actions_template_name=None, empty_listing_actions_template_name=None,
                          extra_context=None, media=None
                          ):
    if media is None:
        media = {
            "js": [], "css": []
        }
    if extra_context is None:
        extra_context = {}

    return type(model.__name__ + 'DynamicListing', (dynamic_list, DynamicListInit), {
        "factory": True,
        'model': model,
        'filterset_class': filterset_class,
        'listing_type': listing_type,
        'listing_actions': listing_actions,
        'table_columns': table_columns,
        'load_rows_from_template': load_rows_from_template,
        'row_template_name': row_template_name,
        "actions_template_name": actions_template_name,
        "empty_listing_actions_template_name": empty_listing_actions_template_name,
        "extra_context": extra_context,
        "media": media,
    })


def dynamic_grid_factory(model, dynamic_list=DynamicGrid, filterset_class=None, listing_type='grid',
                         listing_actions=None, table_columns=None, load_rows_from_template=False,
                         row_template_name=None, extra_context=None, media=None):
    if media is None:
        media = {
            "js": [], "css": []
        }

    if extra_context is None:
        extra_context = {}

    return type(model.__name__ + 'DynamicListing', (dynamic_list, DynamicListInit), {
        "factory": True,
        'model': model,
        'filterset_class': filterset_class,
        'listing_type': listing_type,
        'listing_actions': listing_actions,
        'table_columns': table_columns,
        'load_rows_from_template': load_rows_from_template,
        'row_template_name': row_template_name,
        "extra_context": extra_context,
        "media": media,
    })


def dynamic_list_factory(model, dynamic_list=DynamicList, filterset_class=None, listing_type='list', media=None,
                         extra_context=None, modals_template_name=None, listing_actions=None, item_template_name=None):
    if media is None:
        media = {
            "js": [], "css": []
        }
    if extra_context is None:
        extra_context = {}

    return type(model.__name__ + 'DynamicListing', (dynamic_list, DynamicListInit), {
        "factory": True,
        'model': model,
        'filterset_class': filterset_class,
        'listing_type': listing_type,
        'listing_actions': listing_actions,
        'item_template_name': item_template_name,
        'modals_template_name': modals_template_name,
        'extra_context': extra_context,
        'media': media,
    })


class BaseDynamicListingView(ListView, FilterView):
    title = None
    template_name = 'dynamic_listing/index.html'

    def __init__(self, request=None, queryset=None, *args, **kwargs):
        self.request = self.request
        super(BaseDynamicListingView, self).__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BaseDynamicListingView, self).get_context_data(**kwargs)
        context["breadcrumb"] = self.get_breadcrumb()
        context['title'] = self.get_title()
        return context

    def get_breadcrumb(self):
        return []

    def get_title(self):
        return self.title


class DynamicTableView(BaseDynamicListingView, DynamicTable):
    pass


class DynamicGridView(BaseDynamicListingView, DynamicGrid):
    pass


class DynamicListView(BaseDynamicListingView, DynamicList):
    pass
