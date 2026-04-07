from django.views.generic import ListView
from .models import Post


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
