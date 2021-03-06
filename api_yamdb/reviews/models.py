from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title  # isort:skip
from users.models import User  # isort:skip


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="произведение",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="автор",
    )
    score = models.IntegerField(
        "оценка",
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        error_messages={"validators": "Оценка от 1 до 10!"},
    )
    pub_date = models.DateTimeField(
        "дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "title",
                    "author",
                ),
                name="unique review",
            )
        ]
        ordering = ("pub_date",)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="отзыв",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="автор",
    )
    pub_date = models.DateTimeField(
        "дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
