from django.urls import path

from .views import AuthorPostsListView, HomeView, PostDetailView, PostListView

urlpatterns = [
    path("all-posts/", PostListView.as_view(), name="post_list"),
    path(
        "author/<str:username>",
        AuthorPostsListView.as_view(),
        name="author_posts",
    ),
    path("home/", HomeView.as_view(), name="home"),
    path(
        "post/<str:slug>/<uuid:pk>/",
        PostDetailView.as_view(),
        name="post_detail",
    ),
]
