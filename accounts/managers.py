from time import timezone

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(
        self,
        username,
        email,
        password,
        is_staff,
        is_superuser,
        **extra_fields,
    ):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(
            username,
            email,
            password,
            False,
            False,
            **extra_fields,
        )

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(
            username,
            email,
            password,
            True,
            True,
            **extra_fields,
        )
