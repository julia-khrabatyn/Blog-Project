from django.urls import path

from .views import TagCreateAjaxView

urlpatterns = [
    path(
        "tags/ajax-create/",
        TagCreateAjaxView.as_view(),
        name="tag_ajax_create",
    ),
]
