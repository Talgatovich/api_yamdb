from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .utils import find_length


class UserRole:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLES = [(USER, USER), (MODERATOR, MODERATOR), (ADMIN, ADMIN)]


class User(AbstractUser):
    username = models.TextField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+$", message="Error invalid username"
            )
        ],
    )
    first_name = models.TextField(max_length=150, blank=True)
    last_name = models.TextField(max_length=150, blank=True)
    email = models.EmailField("email address", unique=True, max_length=254)
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=60, blank=True)
    role = models.CharField(
        max_length=find_length(UserRole.ROLES),
        choices=UserRole.ROLES,
        default=UserRole.USER,
    )

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR
