from django.urls import path

from .views import PostListView

urlpatterns = [
    path("posts/list/", PostListView.as_view(), name="post_list"),
]
