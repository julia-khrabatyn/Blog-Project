import magic

from constance import config

from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import FileExtensionValidator


def validate_image_extension(value):
    """Validate file extension."""
    allowed_extensions = config.ALLOWED_IMAGE_EXTENSIONS.split(",")
    validator = FileExtensionValidator(allowed_extensions=allowed_extensions)
    validator(value)


def validate_image_file(value: File):
    """Validate image type and size using magic."""
    value.seek(0)
    max_size = config.MAX_IMAGE_SIZE_MB * 1024 * 1024
    allowed_img_types = config.ALLOWED_IMAGE_TYPES.split(",")
    if value.size > max_size:
        raise ValidationError(
            f"Error! File size must be under {config.MAX_IMAGE_SIZE_MB}!"
        )

    try:
        file_mime = magic.from_buffer(value.read(1024), mime=True)
    except Exception as e:
        raise ValidationError("Could not determine file type!")

    finally:
        value.seek(0)

    if file_mime not in allowed_img_types:
        raise ValidationError(
            f"Error! Incorrect image file type! Upload: {config.ALLOWED_IMAGE_TYPES} files only!"
        )
