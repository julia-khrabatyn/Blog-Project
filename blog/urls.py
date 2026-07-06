from django.urls import path

from core.services.autocomplete import (
    AuthorAutocomplete,
    CategoryAutocomplete,
    PostAutocomplete,
    TagAutocomplete,
)
from .views import (
    AuthorPostsListView,
    CategoryCreateView,
    HomeView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    ToggleLikeView,
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
    path("post/<uuid:pk>/edit/", PostUpdateView.as_view(), name="post_update"),
    path(
        "post/<uuid:pk>/delete/", PostDeleteView.as_view(), name="post_delete"
    ),
    path(
        "category/create/",
        CategoryCreateView.as_view(),
        name="category_create",
    ),
    path("post/<uuid:pk>/like/", ToggleLikeView.as_view(), name="post_like"),
    path(
        "category-autocomplete/",
        CategoryAutocomplete.as_view(),
        name="category-autocomplete",
    ),
    path(
        "tag-autocomplete/", TagAutocomplete.as_view(), name="tag-autocomplete"
    ),
    path(
        "title-autocomplete/",
        PostAutocomplete.as_view(),
        name="post-title-autocomplete",
    ),
    path(
        "author-autocomplete/",
        AuthorAutocomplete.as_view(),
        name="author-autocomplete",
    ),
]
