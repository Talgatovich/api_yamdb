import datetime as dt

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категорий."""
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер жанров."""
    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериалайзер произведений для чтения."""
    category = CategorySerializer(read_only=True,)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre",
                  "category", "rating")
        read_only_fields = fields


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериалайзер произведений для записи."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug",
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre",
                  "category", )

    def validate_year(self, value):
        year = dt.date.today().year
        if not (year - 2000000 < value <= year):
            raise serializers.ValidationError("Проверьте год произведения!")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов."""

    title = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError("Оценка по 10-бальной шкале!")
        return value

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == "POST"
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError("Вы уже написали отзыв!")
        return data

    class Meta:
        fields = "__all__"
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер комментариев."""

    review = serializers.SlugRelatedField(slug_field="text", read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Comment
