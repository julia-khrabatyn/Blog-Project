import nh3


from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Category, Post
from core.services import translate_changed_fields


def _clean_post_text(instance):
    """Protected function for cleaning post text with nh3 for safety reasons."""

    if not instance.text:
        return

    should_clean = False

    if not instance.pk:
        should_clean = True

    else:
        try:
            old_post_text = Post.objects.values_list("text", flat=True).get(
                pk=instance.pk
            )
            if old_post_text != instance.text:
                should_clean = True
        except Post.DoesNotExist:
            should_clean = True

    if should_clean:
        instance.text = nh3.clean(
            instance.text,
            **settings.NH3_POST_SETTINGS,
        )


@receiver(
    pre_save, sender=Post, dispatch_uid="blog.signals.handle_post_pre_save"
)
def handle_post_pre_save(sender, instance, **kwargs):
    """Main function for handling pre_save."""
    _clean_post_text(instance)


@receiver(
    pre_save, sender=Post, dispatch_uid="blog.signals.translate_post_on_save"
)
def translate_post_on_save(sender, instance, **kwargs):
    """Function for handling saving translation for post's title, text, description."""
    translate_changed_fields(
        instance=instance,
        fields_map={
            "title_en": "title_uk",
            "text_en": "text_uk",
            "description_en": "description_uk",
        },
    )


@receiver(
    pre_save,
    sender=Category,
    dispatch_uid="blog.signals.translate_category_on_save",
)
def translate_category_on_save(sender, instance, **kwargs):
    """Function for handling saving translation for category's title"""
    translate_changed_fields(
        instance=instance,
        fields_map={
            "title_en": "title_uk",
        },
    )
