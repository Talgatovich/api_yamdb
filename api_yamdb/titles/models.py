import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

year = dt.date.today().year


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведений."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=256)
    year = models.IntegerField(
        validators=[MinValueValidator(-2000000), MaxValueValidator(int(year))],
        default=None
    )
    description = models.TextField(max_length=500, blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='titles')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name
