from django.db.models import F, OuterRef, Count, Subquery
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Video, Like
from api.permissions import IsOwnerOrPublishedReadOnly
from api.serializers import VideoSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsOwnerOrPublishedReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # ?user_expand=true
        if request.query_params.get('user_expand') == 'true':
            data['owner'] = {
                'id': instance.owner.id,
                'username': instance.owner.username,
            }

        return Response(data)

    def get_queryset(self):
        return (
            Video.objects
            .select_related('owner')
            .only('id', 'name', 'created_at', 'owner_id')
        )

    @action(detail=True, methods=['POST'])
    def likes(self, request, pk=None):
        video = self.get_object()

        if video.owner == request.user:
            return Response(
                {"error": "You cannot like your own video"},
                status=status.HTTP_400_BAD_REQUEST
            )

        like, created = Like.objects.get_or_create(video=video, user=request.user)

        if not created:
            return Response(
                {"error": "You have already liked this video"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Video.object.filter(id=video.id).update(
            total_likes=F('total_likes') + 1
        )

        return Response({"status": "liked"})

    @action(detail=False, methods=['GET'])
    def ids(self):
        ids = Video.objects.filter(
            is_published=True
        ).values_list('id', flat=True)

        return Response(list(ids))

    @action(detail=False, methods=['GET'])
    def statistics_subquery(self):
        likes_subquery = Like.objects.filter(
            video=OuterRef('pk'),
        ).values('video').annotate(
            count=Count('id')
        ).values('count')

        videos = Video.objects.annotate(
            total_likes=Subquery(likes_subquery)
        ).values('id', 'total_likes')

        return Response(list(videos))

    @action(detail=False, methods=['GET'])
    def statistics_group_by(self):
        videos = (
            Video.objects
            .values('id')
            .annotate(total_likes=Count('likes'))
        )

        return Response(list(videos))
