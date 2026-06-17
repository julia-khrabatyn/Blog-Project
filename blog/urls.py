from django.urls import path

from .views import (
    AuthorPostsListView,
    HomeView,
    PostCreateView,
    PostDetailView,
    PostListView,
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path(
        "author/<str:username>/",
        AuthorPostsListView.as_view(),
        name="author_posts",
    ),
    path("", HomeView.as_view(), name="home"),
    path(
        "post/<uuid:pk>/",
        PostDetailView.as_view(),
        name="post_detail",
    ),
]
