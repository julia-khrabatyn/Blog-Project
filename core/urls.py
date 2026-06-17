from django.urls import path

from .views import InlineCreateAjaxView

urlpatterns = [
    path(
        "inline-create/<str:model_name>/",
        InlineCreateAjaxView.as_view(),
        name="inline_create_ajax",
    ),
]
