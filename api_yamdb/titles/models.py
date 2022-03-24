import datetime as dt

from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

year = dt.date.today().year


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50,
                            unique=True,
                            validators=[RegexValidator(
                                regex=r'^[-a-zA-Z0-9_]+$',
                                message="Error invalid slug"
                            )])

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведений."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50,
                            unique=True,
                            validators=[RegexValidator(
                                regex=r'^[-a-zA-Z0-9_]+$',
                                message="Error invalid slug"
                            )])

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.TextField()
    year = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(int(year))],
        default=None
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='titles')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name
