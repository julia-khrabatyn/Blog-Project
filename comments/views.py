import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View


from .forms import CommentForm

__all__ = ["CommentCreateAjaxModelFormView"]


class CommentCreateAjaxModelFormView(LoginRequiredMixin, View):
    """Create Comment View with Ajax."""

    def post(self, request, post_id):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "errors": "Invalid JSON"}, status=400
            )

        form = CommentForm(data)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.user = request.user
            comment.save()
            return JsonResponse({"status": "ok", "text": comment.text})
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )
