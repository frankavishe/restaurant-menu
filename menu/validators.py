from django.core.exceptions import ValidationError

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB


def validate_image_size(file):
    """Reject uploaded images larger than 5MB (FR-009a)."""
    if file.size > MAX_IMAGE_SIZE_BYTES:
        raise ValidationError('Image file too large. Maximum size is 5MB.')
