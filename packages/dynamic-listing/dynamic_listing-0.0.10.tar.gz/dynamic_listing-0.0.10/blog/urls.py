from django.urls import path

from blog.views import BlogTableView

app_name = 'blog'
urlpatterns = [
    path("table/", BlogTableView.as_view(), name="table")
]
