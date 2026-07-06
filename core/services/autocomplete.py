from dal import autocomplete

from accounts.models import User
from blog.models import Category, Post
from tags.models import Tag

__all = [
    "CategoryAutocomplete",
    "TagAutocomplete",
]


class _BaseAutocomplete(autocomplete.AlightQuerySetView):
    "Base class for inheritance."

    model = None

    def get_queryset(self):
        qs = self.model.objects.order_by("title")

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        return qs


class CategoryAutocomplete(_BaseAutocomplete):
    """For plugging autocomplete for categories choice in Post filter's form."""

    model = Category


class PostAutocomplete(_BaseAutocomplete):
    """For plugging autocomplete for categories choice in Post filter's form."""

    model = Post


class TagAutocomplete(_BaseAutocomplete):
    """For plugging autocomplete for tags choice in Post filter's form."""

    model = Tag


class AuthorAutocomplete(autocomplete.AlightQuerySetView):
    """For plugging autocomplete for searching posts by Author in filter's form."""

    def get_queryset(self):
        qs = User.objects.order_by("username")

        if self.q:
            qs = qs.filter(username__icontains=self.q)

        return qs
