from django.db.models import Count
from django.views.generic import ListView

from constance import config

from .models import Post, Category


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
            .order_by("-updated_at")
        )
        return qs


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
