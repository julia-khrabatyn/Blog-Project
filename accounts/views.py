from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch
from django.views.generic import DetailView

from constance import config

from blog.models import Category, Post, Like
from blog.services import generate_single_user_map
from tags.models import Tag

from .models import User

__all__ = [
    "ProfileDetailView",
]


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Show profile info about registered user."""

    model = User
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def _paginate(self, queryset, param_name="page"):
        """Help method for pagination."""
        paginator = Paginator(queryset, config.PAGINATE_BY)
        page_number = self.request.GET.get(param_name)
        return paginator.get_page(page_number)

    def get_queryset(self):
        qs = User.objects.prefetch_related("posts").prefetch_related()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object
        is_own_profile = self.request.user == profile_user
        post_qs = profile_user.posts.prefetch_related(
            "categories",
            "tags",
        )
        published_posts = post_qs.filter(published=True)
        pub_page_obj = self._paginate(published_posts, "page")

        draft_posts = (
            post_qs.filter(published=False)
            if is_own_profile
            else Post.objects.none()
        )
        draft_page_obj = self._paginate(draft_posts, "draft_page")

        if profile_user.latitude and profile_user.longitude:
            user_location = generate_single_user_map(profile_user)

        liked_posts = None
        if is_own_profile:
            liked_post_ids = Like.objects.filter(
                user=profile_user
            ).values_list("post_id", flat=True)
            liked_posts = Post.objects.filter(id__in=liked_post_ids).annotate(
                likes_count=Count("likes")
            )
        context.update(
            {
                "is_own_profile": is_own_profile,
                "page_obj": pub_page_obj,
                "published_posts": pub_page_obj.object_list,
                "published_posts_count": published_posts.count(),
                "draft_page_obj": draft_page_obj,
                "draft_posts": draft_page_obj.object_list,
                "draft_posts_count": draft_posts.count(),
                "categories": Category.objects.filter(
                    posts__user=profile_user,
                ).distinct(),
                "tags": Tag.objects.filter(posts__in=post_qs).distinct(),
                "liked_posts": liked_posts,
                "location": user_location,
            }
        )
        return context
