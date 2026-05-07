import django_filters

from django import forms
from django.apps import (
    apps,
)  # TODO: better use it for avoiding cycle import? do not use: from .models import Post and so on???
from django.contrib.auth import get_user_model

User = get_user_model()
Post = apps.get_model("blog", "Post")
Tag = apps.get_model("tags", "Tag")
Comment = apps.get_model("comments", "Comment")
Category = apps.get_model("blog", "Category")

__all__ = [
    "AuthorPostFilter",
    "BasePostFilter",
    "CommentFilter",
    "GlobalPostFilter",
]


class BasePostFilter(django_filters.FilterSet):
    """Class for filtering Posts by django-filters."""

    # Filter post by title in alphabetic order
    title = django_filters.CharFilter(
        lookup_expr="icontains",
        label="By title ",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter title to filter...",
            }
        ),
    )

    # Filter by tags (when use multiple tags -> find all post that have all provided tags)
    # TODO: Should I change it to Charfield?
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        conjoined=True,
        label="By tags ",
        widget=forms.CheckboxSelectMultiple(),
    )

    # Filter by date
    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="From Date",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
    )
    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="To Date",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        conjoined=True,
        label="By category",
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "start_date",
            "end_date",
            "tags",
        ]


class GlobalPostFilter(BasePostFilter):
    """For sorting Post in general templates."""

    # TODO: Should I change it to Charfield?
    author = django_filters.ModelChoiceFilter(
        field_name="user",
        queryset=User.objects.all(),
        label="Author",
    )

    order_by = django_filters.OrderingFilter(
        fields=(
            ("created_at", "date"),
            ("likes_count", "likes"),
            ("user__username", "author"),
        ),
        field_name="By Author",
        field_labels={"user__username": "By Author"},
    )


class AuthorPostFilter(BasePostFilter):
    """For filtering posts created by Author (without choosing Author)."""

    order_by = django_filters.OrderingFilter(
        fields=(
            ("created_at", "date"),
            ("likes_count", "likes"),
        ),
        field_labels={"created_at": "By date", "likes_count": "Likes"},
    )


class CommentFilter(django_filters.FilterSet):
    """Filter for comments."""

    q = django_filters.CharFilter(
        field_name="text", lookup_expr="icontains", label="Search"
    )

    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="From Date",
    )
    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="To Date",
    )

    author = django_filters.CharFilter(
        field_name="user__username", lookup_expr="icontains", label="Author"
    )

    class Meta:
        model = Comment
        fields = ["q", "author"]
