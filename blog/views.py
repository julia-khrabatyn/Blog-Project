from django.db.models import Count, Exists, OuterRef
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from constance import config

from core.services.like_services import add_liked_annotation

from .filters import AuthorPostFilter, GlobalPostFilter
from .forms import PostForm, CategoryForm
from .models import Category, Like, Post
from .services import (
    get_comments_for_post_view,
    get_filtered_posts,
    generate_users_heatmap,
    generate_single_user_map,
)

User = get_user_model()

__all__ = (
    "AuthorPostsListView",
    "CategoryCreateView",
    "HomeView",
    "PostCreateView",
    "PostDeleteView",
    "PostDetailView",
    "PostListView",
    "PostUpdateView",
    "ToggleLikeView",
)


class AuthorPostsListView(ListView):
    """Display all posts created by this author."""

    model = Post
    template_name = "blog/author_posts_list.html"
    context_object_name = "posts"
    allow_empty = True

    def get_paginate_by(self, queryset):
        return config.PAGINATE_BY

    def get_queryset(self):
        """Get User -> get all user's posts or return 404."""
        self.author = get_object_or_404(User, username=self.kwargs["username"])

        qs = (
            Post.objects.filter(user=self.author, published=True)
            .select_related("user")
            .prefetch_related("categories")
            .annotate(likes_count=Count("likes"))
        )
        qs = add_liked_annotation(qs, self.request.user)

        self.filterset = get_filtered_posts(
            self.request.GET, queryset=qs, filter_class=AuthorPostFilter
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        context["filter"] = self.filterset
        return context


class HomeView(TemplateView):
    """Display main page of Byline-Blog."""

    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        """Show sorted categories by popularity (number of posts in category)"""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        liked_subquery = Like.objects.filter(user=user, post=OuterRef("pk"))

        base_queryset = Post.objects.filter(published=True).select_related(
            "user"
        )

        context["categories"] = Category.objects.annotate(
            posts_count=Count("posts")
        ).order_by("-posts_count")[:5]

        context["popular_posts"] = (
            base_queryset.prefetch_related("categories")
            .annotate(
                likes_count=Count("likes"),
                is_liked=Exists(liked_subquery),
            )
            .order_by("-likes_count", "-updated_at")[:3]
        )
        context["latest_posts"] = (
            base_queryset.prefetch_related("categories")
            .annotate(
                is_liked=Exists(liked_subquery),
            )
            .order_by("-created_at")[:3]
        )

        # generate users_map
        users_with_coordinates = User.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False,
        ).distinct()
        if users_with_coordinates.exists():
            context["heatmap"] = generate_users_heatmap(users_with_coordinates)

        return context


class PostDetailView(DetailView):
    """Display Post details."""

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        """Extract all info about User (post author)."""
        qs = Post.objects.select_related("user")
        return add_liked_annotation(qs, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        author = self.object.user

        comments_page, comment_filter = get_comments_for_post_view(
            post=post,
            query_params=self.request.GET,
            items_per_page=config.COMMENTS_PAGINATION,
        )
        context["comments"] = comments_page
        context["comment_filter"] = comment_filter

        context["latest_author_posts"] = (
            Post.objects.filter(user=author, published=True)
            .exclude(id=self.object.id)
            .order_by("-created_at")[:3]
        )
        if author.latitude and author.longitude:
            context["author_map"] = generate_single_user_map(user=author)

        return context


class PostListView(ListView):
    """Display published posts."""

    model = Post
    template_name = "blog/post_list.html"
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
            .annotate(likes_count=Count("likes"))
        )
        self.filterset = get_filtered_posts(
            self.request.GET, queryset=qs, filter_class=GlobalPostFilter
        )

        qs = self.filterset.qs
        qs = add_liked_annotation(qs, self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Display form for creating category."""

    model = Category
    form_class = CategoryForm
    template_name = "blog/category_create.html"

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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Display form for post creation."""

    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.published = self.request.POST.get("action") == "publish"

        response = super().form_valid(form)

        if self.object.published:
            messages.success(self.request, _("Post published successfully!"))
        messages.success(
            self.request, _("Post successfully saved as a draft!")
        )

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_redirect"] = reverse_lazy("post_list")
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating Post content (updates one field in db by user -> other's automatically thought translation request)."""

    model = Post
    form_class = PostForm
    template_name = "blog/post_update.html"
    success_url = reverse_lazy("post_list")
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def test_func(self):
        """For allowing to update post only by it's own Author!"""
        return self.request.user == self.get_object().user

    def form_valid(self, form):
        action = self.request.POST.get("action")
        if action == "publish":
            form.instance.published = True
        elif action == "draft":
            form.instance.published = False

        return super().form_valid(form)

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_redirect"] = reverse(
            "profile_detail", kwargs={"username": self.request.user.username}
        )
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting post by it's own Author."""

    model = Post
    template_name = "blog/post_delete.html"
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not form.instance.birth_date:
            form.fields["birth_date"].initial = None
        if not form.instance.city:
            form.fields["city"].initial = None
        return form

    def test_func(self):
        """For allowing to delete post only by it's own Author!"""
        post = self.get_object()
        return self.request.user == post.user

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse(
            "profile_detail", kwargs={"username": self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse(
            "profile_detail", kwargs={"username": self.request.user.username}
        )
        return context


class ToggleLikeView(LoginRequiredMixin, View):
    """View for switching like for post."""

    def post(self, request, pk):

        post = get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()

        if like:
            like.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, post=post)
            liked = True

        return JsonResponse(
            {
                "liked": liked,
                "likes_count": post.likes.count(),
            }
        )
