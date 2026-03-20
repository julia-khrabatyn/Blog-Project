from PIL import Image as PilImage
from constance import config

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User


@receiver(post_save, sender=User)
def resize_avatar(sender, instance: User, **kwargs):
    """Resise user's avatar image into constance config size after user save."""
    if not instance.avatar:
        return
    try:
        with PilImage.open(instance.avatar.path) as img:
            image_width = config.AVATAR_WIDTH
            original_width, original_height = img.size
            new_height = int(image_width * original_height / original_width)
            img = img.resize((image_width, new_height), PilImage.LANCZOS)
            img.save(instance.avatar.path)
    except FileNotFoundError:
        pass
    except OSError:
        pass
    except Exception:
        pass
