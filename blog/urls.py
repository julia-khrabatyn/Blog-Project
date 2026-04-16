from django.urls import path

from .views import HomeView, PostDetailView, PostListView

urlpatterns = [
    path("all-posts/", PostListView.as_view(), name="post_list"),
    path("home/", HomeView.as_view(), name="home"),
    path("post/<uuid:pk>/", PostDetailView.as_view(), name="post_detail"),
]
