from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F, Prefetch
from django.core.paginator import Paginator
from django.views.generic import DetailView


from allauth.socialaccount.models import SocialAccount
from constance import config

from blog.models import Category, Post, Like
from blog.services import generate_single_user_map
from tags.models import Tag

from .models import User

__all__ = [
    "ProfileDetailView",
]

PAGINATE_POSTS = config.PAGINATE_BY


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Show profile info about registered user."""

    model = User
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def _paginate(self, queryset, param_name="page"):
        """Help method for pagination."""
        paginator = Paginator(queryset, PAGINATE_POSTS)
        page_number = self.request.GET.get(param_name)
        return paginator.get_page(page_number)

    def get_queryset(self):
        return User.objects.prefetch_related(
            Prefetch(
                "socialaccount_set",
                queryset=SocialAccount.objects.filter(provider="google"),
                to_attr="google_social",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object
        is_own_profile = self.request.user == profile_user

        base_posts = (
            profile_user.posts.select_related("user")
            .prefetch_related("categories", "tags")
            .order_by("-updated_at")
        )

        published_posts = base_posts.filter(published=True)
        draft_posts = (
            base_posts.filter(published=False)
            if is_own_profile
            else Post.objects.none()
        )

        pub_page = self._paginate(published_posts, "page")
        draft_page = self._paginate(draft_posts, "draft_page")

        if profile_user.latitude and profile_user.longitude:
            user_location = generate_single_user_map(profile_user)

        liked_posts = None
        if is_own_profile:
            liked_post_ids = Like.objects.filter(
                user=profile_user
            ).values_list("post_id", flat=True)
            liked_posts = Post.objects.filter(
                id__in=liked_post_ids
            ).select_related("user")

            liked_posts_count = (
                Like.objects.filter(user=profile_user)
                .values("post_id")
                .distinct()
                .count()
            )

        categories = list(
            Category.objects.filter(posts__in=base_posts).distinct()
        )
        tags = list(Tag.objects.filter(posts__in=base_posts).distinct())

        context.update(
            {
                "is_own_profile": is_own_profile,
                "page_obj": pub_page,
                "published_posts": pub_page.object_list,
                "published_posts_count": pub_page.paginator.count,
                "draft_page_obj": draft_page,
                "draft_posts": draft_page.object_list,
                "draft_posts_count": draft_page.paginator.count,
                "categories": categories,
                "tags": tags,
                "liked_posts": liked_posts,
                "liked_posts_count": liked_posts_count,
                "location": user_location,
            }
        )
        return context
