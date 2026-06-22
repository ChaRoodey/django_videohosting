from django.contrib.auth.models import User
from django.db import models


class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    total_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name


class VideoFile(models.Model):
    class Quality(models.TextChoices):
        HD = 'HD', 'HD'
        FHD = 'FHD', 'FHD'
        UHD = 'UHD', 'UHD'

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='videos/')
    quality = models.CharField(choices=Quality.choices, default=Quality.HD, max_length=3)

    class Meta:
        indexes = [
            models.Index(fields=['video']),
        ]


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['video', 'user'],
                name='unique_video_user_like'
            )
        ]

        indexes = [
            models.Index(fields=['video', 'user', 'created_at']),
        ]
