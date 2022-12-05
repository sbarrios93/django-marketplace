import pathlib
import random

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from accounts.models import FollowRequest
from photos.models import Comment, Like, Photo


def get_random_picture():
    pictures = pathlib.Path("fake_images").glob("*.jpg")
    selected = random.choice(list(pictures))
    return selected.open("rb")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    private_profile = factory.Faker("boolean")


class PhotoFactory(DjangoModelFactory):
    class Meta:
        model = Photo

    image = factory.django.ImageField(from_func=get_random_picture)
    caption = factory.Faker("sentence", nb_words=10)
    owner = factory.SubFactory(UserFactory)


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like

    fan = factory.SubFactory(UserFactory)
    photo = factory.SubFactory(PhotoFactory)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(UserFactory)
    photo = factory.SubFactory(PhotoFactory)
    body = factory.Faker("sentence", nb_words=15)


class FollowRequestFactory(DjangoModelFactory):
    class Meta:
        model = FollowRequest
        django_get_or_create = ("sender", "recipient")

    sender = factory.SubFactory(UserFactory)
    recipient = factory.SubFactory(UserFactory)
    approved = factory.Faker("boolean")
