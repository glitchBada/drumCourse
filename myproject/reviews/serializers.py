from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('author_name', 'text', 'photo_url', 'created_at')

    def get_photo_url(self, obj):
        if obj.photo:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        return None