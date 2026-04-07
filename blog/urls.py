from django.urls import path

from .views import HomeView, PostListView

urlpatterns = [
    path("posts/list/", PostListView.as_view(), name="post_list"),
    path("home/", HomeView.as_view(), name="home"),
]
