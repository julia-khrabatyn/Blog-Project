import magic
from django.core.exceptions import ValidationError
from typing import IO

ALLOWED_IMG_TYPES = ["image/jpeg", "image/jpg", "image/webp", "image/png"]
MAX_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_image_file(value: IO):
    """Validate image type and size using magic."""
    if value.size > MAX_SIZE:
        raise ValidationError("Error! File size must be under 5 MB!")

    file_mime = magic.from_buffer(value.read(1024), mime=True)
    value.seek(0)
    if file_mime not in ALLOWED_IMG_TYPES:
        raise ValidationError(
            "Error! Incorrect image file type! Upload .png, .jpg, .jpeg, .webp files only!"
        )
