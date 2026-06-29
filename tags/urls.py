from django.urls import path

from .views import TagCreateView

urlpatterns = [path("tag/create/", TagCreateView.as_view(), name="tag_create")]
