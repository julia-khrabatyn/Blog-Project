import nh3

from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Post


def _clean_post_text(instance):
    """Private function for cleaning post text with nh3 for safety reasons."""

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
