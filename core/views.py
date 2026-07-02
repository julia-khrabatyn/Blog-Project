import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from blog.forms import CategoryForm
from blog.models import Category

from tags.forms import TagForm
from tags.models import Tag

__all__ = [
    "InlineCreateAjaxView",
]

ALLOWED_MODELS = {
    "category": (Category, CategoryForm),
    "tag": (Tag, TagForm),
}


class InlineCreateAjaxView(LoginRequiredMixin, View):
    def post(self, request, model_name):
        if model_name not in ALLOWED_MODELS:
            return JsonResponse(
                {"status": "error", "errors": "Not allowed"}, status=400
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "errors": "Invalid JSON"}, status=400
            )

        _, FormClass = ALLOWED_MODELS[model_name]
        form = FormClass(data)

        if form.is_valid():
            instance = form.save()
            return JsonResponse(
                {"status": "ok", "id": instance.pk, "text": str(instance)}
            )

        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )
