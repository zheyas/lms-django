from django.core.exceptions import ValidationError
import re

def validate_link(value):
    # Проверяем, что ссылка начинается с http или https
    if not re.match(r'^https?://', value):
        raise ValidationError('Ссылка должна начинаться с http:// или https://')
    # Запрещаем ссылки на youtube.com или youtube (по заданию)
    if 'youtube.com' in value or 'youtu.be' in value:
        raise ValidationError('Ссылки на YouTube запрещены')
