from django.urls import path

from .views import CommentCreateAjaxModelFormView

urlpatterns = [
    path(
        "create/<uuid:post_id>/",
        CommentCreateAjaxModelFormView.as_view(),
        name="comment_create_ajax",
    ),
]
