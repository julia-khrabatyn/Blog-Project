from django.urls import path

from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path(
        "<str:username>/", ProfileDetailView.as_view(), name="profile_detail"
    ),
    path(
        "<str:username>/profile/update/",
        ProfileUpdateView.as_view(),
        name="profile_update",
    ),
]
