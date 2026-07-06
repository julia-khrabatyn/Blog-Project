from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from allauth.socialaccount.models import SocialAccount
from constance import config

from blog.models import Category, Post
from blog.services import generate_single_user_map
from core.services.like_services import add_liked_annotation
from tags.models import Tag

from .forms import AvatarUpdateForm, UserProfileForm
from .mixins import UserOwnerMixin
from .models import User

__all__ = [
    "ProfileDetailView",
    "ProfileUpdateView",
]

PAGINATE_POSTS = config.PAGINATE_BY


class ProfileDetailView(LoginRequiredMixin, UserOwnerMixin, DetailView):
    """Display profile info about registered user."""

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
        base_posts = add_liked_annotation(base_posts, self.request.user)

        published_posts = base_posts.filter(published=True)

        draft_posts = (
            base_posts.filter(published=False)
            if is_own_profile
            else Post.objects.none()
        )

        pub_page = self._paginate(published_posts, "page")
        draft_page = self._paginate(draft_posts, "draft_page")

        user_location = None
        if profile_user.latitude and profile_user.longitude:
            user_location = generate_single_user_map(profile_user)

        liked_posts = None
        if is_own_profile:
            # liked_posts = add_liked_annotation(
            #     Post.objects.filter(likes__user=profile_user),
            #     self.request.user,
            # )
            # liked_posts_count = Like.objects.filter(user=profile_user).count()
            liked_posts = add_liked_annotation(
                Post.objects.filter(likes__user=profile_user)
                .select_related("user")
                .prefetch_related("categories", "tags"),
                self.request.user,
            )
            liked_posts_count = liked_posts.count()
        else:
            liked_posts = Post.objects.none()
            liked_posts_count = 0
        # liked_post_ids = Like.objects.filter(
        #     user=profile_user
        # ).values_list("post_id", flat=True)
        # liked_posts = Post.objects.filter(
        #     id__in=liked_post_ids
        # ).select_related("user")

        # liked_posts_count = (
        #     Like.objects.filter(user=profile_user)
        #     .values("post_id")
        #     .distinct()
        #     .count()
        # )

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


class ProfileUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    """View for updating user's info."""

    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile_update.html"
    slug_field = "username"

    def get_queryset(self):
        return User.objects.prefetch_related(
            Prefetch(
                "socialaccount_set",
                queryset=SocialAccount.objects.filter(provider="google"),
                to_attr="google_social",
            )
        ).filter(username=self.kwargs.get(self.slug_url_kwarg))

    def get_success_url(self):
        return reverse_lazy(
            "profile_detail", kwargs={"username": self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_redirect"] = reverse(
            "profile_detail", kwargs={"username": self.request.user.username}
        )
        return context


class AvatarUpdateAjaxView(LoginRequiredMixin, UserOwnerMixin, View):
    """View for avatar updating through AJAX."""

    model = User
    form_class = AvatarUpdateForm

    def post(self, request, *args, **kwargs):
        user = self.target_user

        form = AvatarUpdateForm(
            request.POST,
            request.FILES,
            instance=user,
        )

        print(form.errors)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "avatar_url": f"{user.avatar.url}?v={user.avatar.name}",
                }
            )

        return JsonResponse(
            {
                "status": "error",
                "errors": form.errors,
            },
            status=400,
        )
