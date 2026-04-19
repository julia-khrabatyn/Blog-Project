from django.db.models import Count
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from constance import config

from .models import Post, Category

User = get_user_model()

__all__ = (
    "AuthorPostsListView",
    "HomeView",
    "PostDetailView",
    "PostListview",
)


class AuthorPostsListView(ListView):
    """Display all posts created by this author."""

    model = Post
    template_name = "author_posts_list.html"
    context_object_name = "posts"
    allow_empty = True

    def get_paginate_by(self, queryset):
        return config.PAGINATE_BY

    def get_queryset(self):
        """Get User -> get all user's posts or return 404."""
        self.author = get_object_or_404(User, username=self.kwargs["username"])

        qs = (
            Post.objects.filter(user=self.author)
            .annotate(likes_count=Count("likes"))
            .order_by("-likes_count")
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        return context


class HomeView(ListView):
    """Display main page of Byline-Blog."""

    model = Post
    template_name = "home.html"
    context_object_name = "latest_posts"

    def get_queryset(self):
        """Show users only 3 latest published posts."""
        qs = Post.objects.filter(published=True).order_by("-updated_at")
        return qs[:3]

    def get_context_data(self, **kwargs):
        """Show sorted categories by popularity (number of posts in category)"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(
            posts_count=Count("posts")
        ).order_by("-posts_count")[:5]

        context["popular_posts"] = (
            Post.objects.filter(published=True)
            .annotate(likes_count=Count("likes"))
            .order_by("-likes_count", "-updated_at")[:3]
        )

        return context


class PostDetailView(DetailView):
    """Display Post details."""

    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        """Extract all info about User (post author)."""
        qs = Post.objects.select_related("user")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.object.user
        context["latest_author_posts"] = (
            Post.objects.filter(user=author)
            .exclude(id=self.object.id)
            .order_by("-created_at")[:3]
        )
        return context


class PostListView(ListView):
    """Display published posts."""

    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    allow_empty = True

    def get_paginate_by(self, queryset):
        return config.PAGINATE_BY

    def get_queryset(self):
        """Show users only published posts."""
        qs = (
            Post.objects.filter(published=True)
            .select_related("user")
            .order_by("-created_at")
        )
        return qs
