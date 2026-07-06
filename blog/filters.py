import django_filters

from django import forms

from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy as _p

from dal import autocomplete

from accounts.models import User
from comments.models import Comment
from tags.models import Tag

from .models import Post, Category

__all__ = [
    "AuthorPostFilter",
    "BasePostFilter",
    "CommentFilter",
    "GlobalPostFilter",
]


class BasePostFilter(django_filters.FilterSet):
    """Class for filtering Posts by django-filters."""

    # Filter post by title using autocomplete
    title = django_filters.ModelChoiceFilter(
        queryset=Post.objects.all(),
        label=_("By title"),
        widget=autocomplete.ModelAlight(
            url="post-title-autocomplete",
            attrs={
                "class": "form-control",
                "placeholder": _("Enter title to filter..."),
            },
        ),
    )

    # Filter by tags (when use multiple tags -> find all post that have at least one of the provided tags)
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        conjoined=False,
        label=_("By tags"),
        widget=autocomplete.ModelAlightMultiple(url="tag-autocomplete"),
    )

    # Filter by date
    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label=_("From Date"),
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
    )
    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label=_("To Date"),
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
    )
    # Filter by categories (when use multiple categories -> find all post that have at least one of the provided)
    category = django_filters.ModelMultipleChoiceFilter(
        field_name="categories",
        queryset=Category.objects.all(),
        conjoined=False,
        label=_("By category"),
        widget=autocomplete.ModelAlightMultiple(url="category-autocomplete"),
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


class AuthorPostFilter(BasePostFilter):
    """For filtering posts created by Author (without choosing Author)."""

    ORDERING_FIELDS = (
        ("created_at", "date"),
        ("likes_count", "likes"),
        ("comments_count", "discussion_popularity"),
    )

    ORDERING_LABELS = {
        "created_at": _("By date"),
        "likes_count": _p("filter", "Likes"),
        "comments_count": _("By discussion popularity"),
    }

    order_by = django_filters.OrderingFilter(
        fields=ORDERING_FIELDS,
        label=_("Order by"),
        field_labels=ORDERING_LABELS,
    )


class GlobalPostFilter(AuthorPostFilter):
    """For sorting Post in general templates."""

    ORDERING_FIELDS = AuthorPostFilter.ORDERING_FIELDS + (
        ("user__username", "author"),
    )

    ORDERING_LABELS = {
        **AuthorPostFilter.ORDERING_LABELS,
        "user__username": _p("filter", "By Author"),
    }

    order_by = django_filters.OrderingFilter(
        fields=ORDERING_FIELDS,
        label=_("Order by"),
        field_labels=ORDERING_LABELS,
    )

    author = django_filters.ModelChoiceFilter(
        field_name="user",
        queryset=User.objects.all(),
        label=_p("filter", "By Author"),
        widget=autocomplete.ModelAlight(url="author-autocomplete"),
    )


class CommentFilter(django_filters.FilterSet):
    """Filter for comments."""

    q = django_filters.CharFilter(
        field_name="text",
        lookup_expr="icontains",
        label=_("Search"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Search comments..."),
            },
        ),
    )

    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label=_("From Date"),
    )
    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label=_("To Date"),
    )

    author = django_filters.ModelChoiceFilter(
        field_name="user",
        queryset=User.objects.all(),
        label=_p("filter", "By Author"),
        widget=autocomplete.ModelAlight(url="author-autocomplete"),
    )

    class Meta:
        model = Comment
        fields = ["q", "author", "start_date", "end_date"]
