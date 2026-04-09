from django.db.models import Count
from django.views.generic import ListView

from .models import Post, Category


class PostListView(ListView):
    """Display published posts."""

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]
    allow_empty = True
    paginate_by = 5

    def get_queryset(self):
        """Show users only published posts."""
        return (
            Post.objects.filter(published=True)
            .select_related("user")
            .order_by("-updated_at")
        )


class HomeView(ListView):
    """Display main page of Byline-Blog."""

    model = Post
    template_name = "home.html"
    context_object_name = "latest_posts"

    def get_queryset(self):
        """Show users only 3 latest published posts."""
        return Post.objects.filter(published=True).order_by("-updated_at")[:3]

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
