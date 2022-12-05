from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Q

from accounts.managers import CustomUserManager
from photos.models import Comment, Like, Photo


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=128)
    private_profile = models.BooleanField(default=False)

    # permissions
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS: list[str] = ["email", "private_profile"]

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def like_count(self):
        return Like.objects.filter(fan_id=self).count()

    def comment_count(self):
        return Comment.objects.filter(author_id=self).count()

    def __str__(self):
        return self.username

    def follower_count(self):
        return FollowRequest.objects.filter(
            Q(recipient=self) & Q(approved=True)
        ).count()

    def following_count(self):
        return FollowRequest.objects.filter(Q(sender=self) & Q(approved=True)).count()

    def photos(self):
        return Photo.objects.filter(owner=self)

    def like_photo(self, photo_id):
        like = Like.objects.create(fan=self, photo=Photo.objects.get(id=photo_id))
        like.save()

    def unlike_photo(self, photo_id):
        Like.objects.filter(fan=self, photo=photo_id).delete()

    def get_liked_photos(self):
        return Like.objects.filter(fan=self).values_list("photo", flat=True)

    @property
    def user_username(self):
        self.username

    def send_follow_request(self, recipient):
        if recipient != self:
            if recipient.private_profile:
                FollowRequest.objects.create(
                    sender=self, recipient=recipient, approved=False
                )
            else:
                FollowRequest.objects.create(
                    sender=self, recipient=recipient, approved=True
                )

    def remove_following(self, following):
        FollowRequest.objects.filter(sender=self, recipient=following).delete()

    def approve_follow_request(self, sender):
        FollowRequest.objects.filter(sender=sender).update(approved=True)

    def reject_follow_request(self, sender):
        FollowRequest.objects.filter(sender=sender).delete()

    def get_following(self):
        return FollowRequest.objects.filter(sender=self).values_list(
            "recipient", flat=True
        )

    def get_pending_follow_requests(self):
        return FollowRequest.objects.filter(
            Q(sender=self) & Q(approved=False)
        ).values_list("recipient", flat=True)

    def get_followers(self):
        return FollowRequest.objects.filter(recipient=self).values_list(
            "sender", flat=True
        )


class FollowRequest(models.Model):
    sender = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name="sender"
    )
    recipient = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name="recipient"
    )
    approved = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "recipient"], name="unique_requests"
            )
        ]
