from django.urls import path

from .views import ProfileDetailView, ProfileUpdateView, AvatarUpdateAjaxView

urlpatterns = [
    path(
        "<str:username>/", ProfileDetailView.as_view(), name="profile_detail"
    ),
    path(
        "<str:username>/profile/update/",
        ProfileUpdateView.as_view(),
        name="profile_update",
    ),
    path(
        "<str:username>/avatar/update/",
        AvatarUpdateAjaxView.as_view(),
        name="change_avatar",
    ),
]
