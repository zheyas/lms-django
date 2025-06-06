import re
from django.core.exceptions import ValidationError

def validate_link(value):
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
    if value and not re.match(youtube_regex, value):
        raise ValidationError('Разрешены только ссылки на YouTube!')
