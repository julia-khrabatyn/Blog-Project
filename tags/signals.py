from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Tag
from core.services import translate_changed_fields, get_translation_field_map


@receiver(
    pre_save,
    sender=Tag,
    dispatch_uid="blog.signals.translate_tag_on_save",
)
def translate_category_on_save(sender, instance, **kwargs):
    """Function for handling saving translation for tag's title"""
    translate_changed_fields(
        instance=instance, fields_map=get_translation_field_map(["title"])
    )
