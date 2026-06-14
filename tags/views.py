from django.shortcuts import render

from blog.views import _BaseCreateAjaxView

from .models import Tag


class TagCreateAjaxView(_BaseCreateAjaxView):
    model = Tag
