from django.db.models import BooleanField, Count, Exists, OuterRef, Value

from blog.models import Like

__all__ = [
    "add_liked_annotation",
]


# def add_liked_annotation(queryset, user):
# queryset = queryset.annotate(likes_count=Count("likes", distinct=True))

# if not user.is_authenticated:
#     return queryset.annotate(
#         is_liked=Value(False, output_field=BooleanField())
#     )

# liked_subquery = Like.objects.filter(user=user, post=OuterRef("pk"))


# return queryset.annotate(is_liked=Exists(liked_subquery))
def add_liked_annotation(queryset, user):
    queryset = queryset.annotate(likes_count=Count("likes", distinct=True))
    if not user.is_authenticated:
        return queryset.annotate(
            is_liked=Value(False, output_field=BooleanField())
        )

    liked_subquery = Like.objects.filter(
        user=user,
        post=OuterRef("pk"),
    )

    return queryset.annotate(is_liked=Exists(liked_subquery))
