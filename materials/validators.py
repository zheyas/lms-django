import re

from rest_framework import serializers

YOUTUBE_REGEX = re.compile(r"https?://(www\.)?youtube\.com/|https?://youtu\.be/")


def youtube_only_validator(value):
    if value and not YOUTUBE_REGEX.match(value):
        raise serializers.ValidationError(
            "Разрешены только ссылки на youtube.com или youtu.be"
        )
