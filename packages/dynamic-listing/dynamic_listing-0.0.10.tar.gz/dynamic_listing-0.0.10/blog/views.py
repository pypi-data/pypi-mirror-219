from blog.models import Blog
from src.dynamic_listing.views import DynamicTableView


class BlogTableView(DynamicTableView):
    model = Blog
    title = "Blogs"
    row_template_name = 'blog/table/_table_row.html'
    load_rows_from_template = True
    table_columns = (
        ('id', "ID"),
        ('title', "Title", "text-start max-w-200px"),
        ('content', "Content", "text-center max-w-200px"),
        ('category', "Category", "text-center"),
        ('tags', "Tags", "text-center"),
    )

    def get_breadcrumb(self):
        return [
            {"title": "Home", "url": '/'},
            {"title": "Blogs"},
            {"title": "Table"}
        ]
