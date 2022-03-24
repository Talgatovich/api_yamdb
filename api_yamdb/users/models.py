from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

CHOISES = [("user", "User"), ("moderator", "Moderator"), ("admin", "Admin")]


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)
    bio = models.TextField(max_length=300, blank=True)
    confirmation_code = models.CharField(max_length=60, blank=True)
    role = models.CharField(max_length=25, choices=CHOISES, default="user")


    class Meta:
        constraints = [
            UniqueConstraint(fields=["username", "email"], name="unique_user")
        ]

    def is_admin(self):
        return self.role == "admin" or self.is_staff

    def is_moderator(self):
        return self.role == "moderator"
