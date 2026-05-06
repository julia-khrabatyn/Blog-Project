from django.db.models import Count
from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from constance import config

from .models import Post, Category
from .services import generate_users_heatmap, generate_single_user_map

# TODO: maybe in django-constance? 
# TODO або в сетінгси
COMMENT_PAGINATION = 5

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
            Post.objects.filter(user=self.author) # TODO Що робити з постами у якиз паблішт - фолс???
            .select_related("user")
            .prefetch_related("categories")
            .annotate(likes_count=Count("likes"))
            .order_by("-likes_count", "updated_at")
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        return context


class HomeView(TemplateView):
    """Display main page of Byline-Blog."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """Show sorted categories by popularity (number of posts in category)"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(
            posts_count=Count("posts")
        ).order_by("-posts_count")[:5]

        context["popular_posts"] = (
            Post.objects.filter(published=True)
            .select_related("user")
            .prefetch_related("categories")
            .annotate(likes_count=Count("likes"))
            .order_by("-likes_count", "-updated_at")[:3]
        )
        context["latest_posts"] = (
            Post.objects.filter(published=True)
            .select_related("user")
            .prefetch_related("categories")
            .order_by("-created_at")[:3]
        )
        # generate usersmap
        users_with_coordinates = User.objects.filter(
            latitude__isnull=False
        ).distinct()
        if users_with_coordinates.exists():
            context["heatmap"] = generate_users_heatmap(users_with_coordinates)

        return context


class PostDetailView(DetailView):
    """Display Post details."""

    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        """Extract all info about User (post author)."""
        qs = Post.objects.select_related("user").prefetch_related(
            "comments__user"
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        author = self.object.user

        # TODO: should i move it ?
        all_comments = post.comments.all()
        search_query = self.request.GET.get("q")
        if search_query:
            all_comments = all_comments.filter(text__icontains=search_query)

        paginator = Paginator(all_comments, COMMENT_PAGINATION)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["comments"] = page_obj
        context["search_query"] = search_query

        # TODO перенести до перед створення пагінатора, бо до об'єкту пейджа не 
        # застосується це сортування і об'єднати разом з фільтром потім соворити об'єкт пагінатора
        sort = self.request.GET.get("sort", "-created_at")
        if sort in ["created_at", "-created_at"]:
            all_comments = all_comments.order_by(sort)

        context["latest_author_posts"] = (
            Post.objects.filter(user=author)
            .exclude(id=self.object.id)
            .order_by("-created_at")[:3]
        )
        if author.latitude and author.longitude:
            context["author_map"] = generate_single_user_map(user=author)
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
            .prefetch_related("categories")
            .order_by("-created_at")
        )
        return qs
