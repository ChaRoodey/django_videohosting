from rest_framework import serializers

from api.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'total_likes')
