from rest_framework import serializers
from urllib.parse import urlparse


def validate_youtube_url(value):
    """Валидатор для проверки, что ссылка ведет только на YouTube"""
    if value:
        parsed_url = urlparse(value)
        if parsed_url.hostname not in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            raise serializers.ValidationError("Разрешены только ссылки на YouTube")
    return value