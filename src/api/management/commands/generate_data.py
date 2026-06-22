from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Video, Like
import random

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if Video.objects.exists():
            self.stdout.write("Data already exists, skipping")
            return

        users = []

        # 10k users
        for i in range(100):
            u = User.objects.create_user(
                username=f"user{i}",
                password="test123"
            )
            users.append(u)

        videos = []

        # 100k videos
        for i in range(100):
            v = Video.objects.create(
                owner=random.choice(users),
                name=f"video_{i}",
                is_published=True,
                total_likes=0
            )
            videos.append(v)

        # realistic likes
        for v in videos:
            for _ in range(random.randint(0, 5)):
                Like.objects.get_or_create(
                    video=v,
                    user=random.choice(users)
                )

        self.stdout.write("Data generated successfully")
