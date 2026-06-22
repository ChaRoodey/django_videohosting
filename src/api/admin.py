from django.contrib import admin

from api.models import Video, Like, VideoFile


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'is_published',
        'total_likes',
        'created_at',
    )

    list_filter = (
        'is_published',
        'created_at',
        'owner',
    )

    search_fields = (
        'name',
        'owner__username',
    )

    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('owner').prefetch_related('files', 'likes')


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'video',
        'quality',
        'file',
    )

    list_filter = (
        'quality',
    )

    search_fields = (
        'video__name',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('video')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'video',
        'user',
    )

    list_filter = (
        'video',
        'user',
    )

    search_fields = (
        'video__name',
        'user__username',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('video', 'user')
