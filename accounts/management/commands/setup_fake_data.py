import random

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import CustomUser, FollowRequest
from factories import (
    CommentFactory,
    FollowRequestFactory,
    LikeFactory,
    PhotoFactory,
    UserFactory,
)
from photos.models import Comment, Like, Photo

NUM_USERS = 50
NUM_PHOTOS = 100
COMMENTS_PER_IMAGE = 10
LIKES_PER_IMAGE = 50
REQUESTS_PER_USER = 10


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [CustomUser, Photo, Comment, Like, FollowRequest]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        people = []
        for _ in range(NUM_USERS):
            person = UserFactory()
            people.append(person)

        for _ in range(NUM_PHOTOS):
            photo = PhotoFactory(owner=random.choice(people))
            for _ in range(COMMENTS_PER_IMAGE):
                CommentFactory(photo=photo, author=random.choice(people))
            for _ in range(LIKES_PER_IMAGE):
                LikeFactory(photo=photo, fan=random.choice(people))

        for person in people:
            people_except_self = [p for p in people if p != person]
            for _ in range(REQUESTS_PER_USER):
                FollowRequestFactory(
                    sender=person,
                    recipient=random.choice(people_except_self),
                )
