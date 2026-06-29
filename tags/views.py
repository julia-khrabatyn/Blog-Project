from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .forms import TagForm
from .models import Tag

__all__ = ["TagCreateView"]


class TagCreateView(LoginRequiredMixin, CreateView):
    """Display form for creating tag."""

    model = Tag
    form_class = TagForm
    template_name = "tags/tag_create.html"

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
